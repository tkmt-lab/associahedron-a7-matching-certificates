#!/usr/bin/env python3
"""Verify saved evidence. This program never calls a SAT solver."""
import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

P = Path(__file__).resolve().parent
sys.path.insert(0, str(P / 'scripts'))
from graph_models import construct
from encode import graph as lower_graph
from strengthen import strengthened


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''):
            h.update(b)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def lrat_success(result):
    return result.returncode == 0 and result.stdout.strip() == 's VERIFIED UNSAT'


def main():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled; do not use python -O')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lrat', type=Path, help='Local A7-k133-vertex.lrat.gz archive')
    ap.add_argument('--checker', type=Path, help='Locally built cake_lpr executable')
    ap.add_argument('--output', type=Path, help='Optional JSON receipt (no local paths recorded)')
    ap.add_argument('--budget-seconds', type=float, default=540)
    args = ap.parse_args()
    if bool(args.lrat) != bool(args.checker):
        ap.error('--lrat and --checker are required together')
    if not 0 < args.budget_seconds <= 600:
        ap.error('budget must be in (0, 600] seconds')
    start = time.monotonic()
    deadline = start + args.budget_seconds
    def run(command, required=True):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('verification budget exhausted')
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                timeout=remaining, env={**os.environ, 'OMP_NUM_THREADS':'1'})
        if required and result.returncode != 0:
            raise RuntimeError('Verifier failed: ' + Path(command[0]).name + '\n' + result.stderr[:1000])
        return result
    manifest = read(P / 'MANIFEST.json')
    expected_paths = {e['path'] for e in manifest['files']}
    assert len(expected_paths) == len(manifest['files'])
    for e in manifest['files']:
        f = P / e['path']
        assert f.resolve().is_relative_to(P), 'Manifest path outside packet'
        assert f.stat().st_size == e['bytes'] and sha(f) == e['sha256'], e['path']
    g, polygon_edges = construct()
    stored = read(P / 'data/graph.json')
    assert g == stored
    polygon_text = '429 1287\n' + ''.join(f'{u} {v}\n' for u, v in polygon_edges)
    assert polygon_text == (P / 'data/polygon-graph.txt').read_text()
    result = {'status':'PASS', 'scope':'Graph, matching witnesses, C9 finite certificate, CNF regeneration',
              'python':platform.python_version(), 'platform':platform.system() + '-' + platform.machine(),
              'graph':{'vertices':429, 'edges':1287, 'degree':6, 'two_generation_methods_agree':True},
              'upper':[], 'negative_controls':[], 'lrat_replayed':False,
              'new_SAT_search':False, 'independent_agent_review':False}
    cache = P / '.cache'
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='verify-', dir=cache) as td:
        td = Path(td)
        checker_b = td / 'check-matching'
        run(['c++', '-O2', '-std=c++17', P / 'scripts/check_matching.cpp', '-o', checker_b])
        result['cpp_flags'] = '-O2 -std=c++17'
        result['cpp_checker_sha256'] = sha(checker_b)
        for k in [143, 144, 156]:
            candidate = P / f'data/matchings/matching-{k}.json'
            text_file = P / f'data/matchings/matching-{k}.txt'
            a = read(candidate)
            lines = text_file.read_text().splitlines()
            assert int(lines[0]) == len(lines)-1 == k
            assert [list(map(int, line.split())) for line in lines[1:]] == a['matching']
            ca = json.loads(run([sys.executable, '-B', P/'scripts/check_matching.py', P/'data/graph.json', candidate]).stdout)
            cb = json.loads(run([checker_b, P/'data/polygon-graph.txt', text_file]).stdout)
            assert ca['verdict'] == cb['verdict'] == 'PASS'
            assert ca['matching_size'] == cb['matching_size'] == k
            result['upper'].append({'matching_size':k, 'candidate_json_sha256':sha(candidate),
                                    'candidate_text_sha256':sha(text_file), 'checker_a':ca, 'checker_b':cb})
        # Check the upper witness within the exact symmetry scope of the lower certificate.
        lookup = {frozenset(map(tuple,t)):i for i,t in enumerate(g['triangulations'])}
        matching = {tuple(sorted(e)) for e in read(P/'data/matchings/matching-144.json')['matching']}
        for k in range(9):
            perm = [lookup[frozenset(tuple(sorted(((a+k)%9,(b+k)%9))) for a,b in t)] for t in g['triangulations']]
            assert {tuple(sorted((perm[a],perm[b]))) for a,b in matching} == matching
        result['C9_witness_invariant_under_all_9_rotations'] = True
        result['C9_certificate'] = json.loads(run([sys.executable, '-B', P/'scripts/check_c9_certificate.py']).stdout)
        assert result['C9_certificate']['C9_invariant_lower_bound'] == 144
        base = read(P/'data/matchings/matching-143.json')
        edges = {tuple(sorted(e)) for e in g['edges']}
        u, v = base['matching'][0]
        w = next(x for x in range(len(g['vertices']))
                 if x != v and tuple(sorted((u, x))) in edges)
        nonedge = next((a, b) for a in range(len(g['vertices']))
                       for b in range(a + 1, len(g['vertices'])) if (a, b) not in edges)
        cases = {'duplicate_endpoint':[[u, v], [u, w]],
                 'nonedge':[list(nonedge)], 'not_maximal':base['matching'][1:]}
        result['matching_negative_control_inputs'] = {
            'duplicate_endpoint':cases['duplicate_endpoint'], 'nonedge':cases['nonedge'],
            'not_maximal_removed_edge':base['matching'][0],
            'not_maximal_remaining_edges':len(cases['not_maximal'])}
        for name, pairs in cases.items():
            bad = copy.deepcopy(base)
            bad['matching'], bad['size'] = pairs, len(pairs)
            (td/'bad.json').write_text(json.dumps(bad))
            (td/'bad.txt').write_text(str(len(pairs))+'\n'+''.join(f'{u} {v}\n' for u,v in pairs))
            for label, cmd in [('python', [sys.executable,'-B',P/'scripts/check_matching.py',P/'data/graph.json',td/'bad.json']),
                               ('cpp',[checker_b,P/'data/polygon-graph.txt',td/'bad.txt'])]:
                assert run(cmd, required=False).returncode != 0
                result['negative_controls'].append(name+'_'+label+'_rejected')
        cert = read(P/'data/c9/c9-no17-certificate.json')
        for name in ['missing_allowed_orbit', 'wrong_target', 'wrong_branch']:
            bad = copy.deepcopy(cert)
            if name == 'missing_allowed_orbit':
                bad['allowed'].pop()
            elif name == 'wrong_target':
                bad['target'] = 16
            else:
                assert 'branch' in bad['proof']
                bad['proof']['branch'] = -1
            (td/'bad-c9.json').write_text(json.dumps(bad))
            assert run([sys.executable,'-B',P/'scripts/check_c9_certificate.py','--certificate',td/'bad-c9.json'],required=False).returncode != 0
            result['negative_controls'].append(name+'_rejected')
        lg = lower_graph(7)
        assert lg['vertices'] == g['vertices'] and [list(e) for e in lg['edges']] == g['edges']
        assert [list(map(list,t)) for t in lg['triangulations']] == g['triangulations']
        cnf = td/'A7-k133.cnf'
        strengthened(lg, 133, False).save(cnf)
        entry = next(e for e in read(P/'data/lower/certificates.json')['certificates'] if e['k']==133)
        assert sha(cnf) == sha(P/'data/lower/A7-k133.cnf') == entry['cnf_sha256']
        result['lower_cnf'] = {'k':133, 'sha256':entry['cnf_sha256'], 'regenerated':True, 'no_symmetry_breaking':True}
        if args.lrat:
            archive, checker = args.lrat.resolve(), args.checker.resolve()
            assert archive.stat().st_size == entry['gzip_bytes'] and sha(archive) == entry['gzip_sha256']
            raw = td/'proof.lrat'
            raw_hash = hashlib.sha256()
            with gzip.open(archive, 'rb') as src, raw.open('wb') as dst:
                for block in iter(lambda:src.read(2**20), b''):
                    if time.monotonic() >= deadline:
                        raise TimeoutError('verification budget exhausted during decompression')
                    dst.write(block)
                    raw_hash.update(block)
            assert raw.stat().st_size == entry['raw_bytes'] and raw_hash.hexdigest() == entry['raw_sha256']
            checked = run([checker,'--CML_HEAP_SIZE=1536','--CML_STACK_SIZE=128',cnf,raw])
            assert lrat_success(checked), 'Missing exact cake_lpr success marker'
            result['lrat_replayed'] = True
            result['scope'] += ', saved binary LRAT replay with cake_lpr'
            result['lrat'] = {'k':133,'archive_sha256':entry['gzip_sha256'],'raw_sha256':entry['raw_sha256'],
                              'checker_sha256':sha(checker),'stdout':checked.stdout.strip(),
                              'guaranteed_layer':'UNSAT of this CNF; graph/encoding correspondence is documented separately'}
            (td/'empty.lrat').write_bytes(b'')
            bad = run([checker,'--CML_HEAP_SIZE=1536','--CML_STACK_SIZE=128',cnf,td/'empty.lrat'],required=False)
            assert not lrat_success(bad)
            result['negative_controls'].append('empty_lrat_rejected_by_exact_marker_check')
        result['seconds'] = time.monotonic() - start
        assert result['seconds'] <= args.budget_seconds
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
