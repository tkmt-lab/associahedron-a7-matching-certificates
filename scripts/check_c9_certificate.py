"""Standalone finite certificate verifier. Imports no search/model builder.
Reconstructs C9 action and matching-lift availability directly from the graph.
"""
import argparse,hashlib,itertools,json,sys
from pathlib import Path

def main():
    if sys.flags.optimize:raise RuntimeError('Assertions must be enabled; do not use python -O')
    p=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=p/'data/c9/c9-no17-certificate.json');args=ap.parse_args()
    raw=(p/'data/graph.json').read_bytes();g=json.loads(raw)
    cert=json.loads(args.certificate.read_text());assert cert['graph_sha256']==hashlib.sha256(raw).hexdigest()
    lookup={frozenset(map(tuple,t)):i for i,t in enumerate(g['triangulations'])}
    perms=[]
    for k in range(9):
        perms.append([lookup[frozenset(tuple(sorted(((u+k)%9,(v+k)%9))) for u,v in t)] for t in g['triangulations']])
    graph_edges={frozenset(e) for e in g['edges']}
    assert all({frozenset((perm[u],perm[v])) for u,v in g['edges']}==graph_edges for perm in perms)
    partition=[];assigned={}
    for v in range(429):
        if v in assigned:continue
        orbit={perm[v] for perm in perms};assert not orbit&assigned.keys()
        for u in orbit:assigned[u]=len(partition)
        partition.append(orbit)
    assert len(partition)==49
    adjacent={i:set() for i in range(49)};can_match=set();weights=set()
    for u,v in g['edges']:
        a,b=assigned[u],assigned[v];adjacent[a].add(b);adjacent[b].add(a)
        orbit={tuple(sorted((perm[u],perm[v]))) for perm in perms}
        ends=[z for e in orbit for z in e]
        if len(ends)==len(set(ends)):
            assert a!=b and set(ends)==partition[a]|partition[b]
            can_match.update((a,b));weights.add(len(orbit))
    assert weights=={9} and len(can_match)==47
    mandatory=set(range(49))-can_match;assert len(mandatory)==2
    assert all(len(partition[v])==9 for v in can_match)
    assert all(len(partition[v])==3 for v in mandatory)
    assert all(not adjacent[u]&mandatory for u in mandatory)
    allowed=can_match-set().union(*(adjacent[u] for u in mandatory))
    assert len(allowed)==43 and sorted(mandatory)==cert['mandatory_unmatched'] and sorted(allowed)==cert['allowed']
    assert cert['target']==17
    visited=0
    def verify(node,vertices,target):
        nonlocal visited
        visited+=1;assert target>0
        if set(node)=={'cover'}:
            parts=node['cover'];flat=[v for part in parts for v in part]
            assert all(type(v) is int for v in flat)
            assert len(set(flat))==len(flat) and set(flat)==vertices
            assert len(parts)<target and all(part for part in parts)
            for part in parts:
                assert all(v in adjacent[u] for u,v in itertools.combinations(part,2))
        else:
            assert set(node)=={'branch','exclude','include'}
            v=node['branch'];assert type(v) is int and v in vertices
            verify(node['exclude'],vertices-{v},target)
            verify(node['include'],vertices-{v}-adjacent[v],target-1)
    verify(cert['proof'],allowed,17);assert visited==cert['nodes']
    # At most 15 selected edge orbits (135 original edges) would cover at
    # most 30 of the 47 active vertex orbits, leaving >=17 in allowed.
    result={'verdict':'PASS','certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
            'nodes':visited,'active_orbits':47,'mandatory_unmatched_orbits':2,'allowed_unmatched_orbits':43,
            'forbidden_independent_size':17,'C9_invariant_lower_bound':144,
            'scope':'C9-invariant maximal matchings only; no unrestricted lower-bound claim',
            'formal_proof':False,'separate_search_free_verifier':True}
    print(json.dumps(result))

if __name__=='__main__':main()
