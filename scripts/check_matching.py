"""Exact checker A: tree graph, endpoint set, unmatched induced edge set."""
import json,sys,hashlib
from pathlib import Path

def check(graph,candidate):
    n=len(graph['vertices']);edges={frozenset(e) for e in graph['edges']};used=set()
    pairs=candidate['matching']
    for pair in pairs:
        if not isinstance(pair,list) or len(pair)!=2 or any(type(v) is not int or v<0 or v>=n for v in pair):raise ValueError('malformed edge')
        a,b=pair
        if a==b or frozenset(pair) not in edges:raise ValueError('not a graph edge')
        if a in used or b in used:raise ValueError('endpoint reused')
        used.update(pair)
    missing=[list(e) for e in edges if not e & used]
    if missing:raise ValueError('not maximal')
    return {'verdict':'PASS','matching_size':len(pairs),'unmatched_vertices':n-len(used),'uncovered_edges':0}

def main():
    graph=Path(sys.argv[1]);cand=Path(sys.argv[2]);g=json.loads(graph.read_text());c=json.loads(cand.read_text())
    assert c['graph_sha256']==hashlib.sha256(graph.read_bytes()).hexdigest()
    r=check(g,c);r['candidate_sha256']=hashlib.sha256(cand.read_bytes()).hexdigest()
    print(json.dumps(r))
if __name__=='__main__':main()
