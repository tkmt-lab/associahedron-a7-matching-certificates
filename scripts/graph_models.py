"""Two constructions of A7, linked by the leaf-interval bijection.
No matching constructions or literature algorithms were consulted.
"""
from functools import lru_cache
from pathlib import Path
import json,hashlib

@lru_cache(None)
def trees(n):
    if n==0:return (None,)
    return tuple((l,r) for k in range(n) for l in trees(k) for r in trees(n-1-k))

def encode(t):return '.' if t is None else '('+encode(t[0])+encode(t[1])+')'

def rotations(t):
    if t is None:return set()
    a,b=t;result=set()
    if a is not None:result.add((a[0],(a[1],b)))
    if b is not None:result.add(((a,b[0]),b[1]))
    result.update((x,b) for x in rotations(a))
    result.update((a,x) for x in rotations(b))
    return result

def intervals(t):
    diagonals=[]
    def walk(x,start):
        if x is None:return start+1
        middle=walk(x[0],start);end=walk(x[1],middle)
        if (start,end)!=(0,8):diagonals.append((start,end))
        return end
    assert walk(t,0)==8
    return tuple(sorted(diagonals))

def flips(triangulation):
    # Triangle incidence, independently of the tree recursion/rotation routine.
    edges=set(triangulation)|{tuple(sorted((i,(i+1)%9))) for i in range(9)}
    result=set()
    for a,b in triangulation:
        opposite=[c for c in range(9) if c not in (a,b)
                  and tuple(sorted((a,c))) in edges and tuple(sorted((b,c))) in edges]
        assert len(opposite)==2
        new=tuple(sorted(opposite))
        assert new not in edges
        result.add(tuple(sorted((set(triangulation)-{(a,b)})|{new})))
    return result

def construct():
    ts=sorted(trees(7),key=encode);idx={t:i for i,t in enumerate(ts)}
    tree_edges={tuple(sorted((i,idx[u]))) for i,t in enumerate(ts) for u in rotations(t)}
    fan=tuple((0,k) for k in range(2,8));seen={fan};stack=[fan];poly_edges=set()
    while stack:
        a=stack.pop()
        for b in flips(a):
            poly_edges.add(tuple(sorted((a,b))))
            if b not in seen:seen.add(b);stack.append(b)
    mapped={intervals(t):i for i,t in enumerate(ts)}
    assert len(mapped)==len(ts)==len(seen)==429 and set(mapped)==seen
    translated={tuple(sorted((mapped[a],mapped[b]))) for a,b in poly_edges}
    assert tree_edges==translated and len(tree_edges)==1287
    degree=[0]*429
    for a,b in tree_edges:degree[a]+=1;degree[b]+=1
    assert set(degree)=={6}
    return {'vertices':[encode(t) for t in ts],
            'triangulations':[list(map(list,intervals(t))) for t in ts],
            'edges':[list(e) for e in sorted(tree_edges)]},sorted(translated)

def main():
    p=Path(__file__).resolve().parent
    g,poly=construct();raw=(json.dumps(g,separators=(',',':'))+'\n').encode()
    (p/'graph.json').write_bytes(raw)
    # Checker B consumes the graph from the polygon construction independently.
    lines=['429 1287']+['%d %d'%e for e in poly]
    (p/'polygon-graph.txt').write_text('\n'.join(lines)+'\n')
    result={'vertices':429,'edges':1287,'degree':6,'tree_to_polygon_bijection':True,
            'edge_sets_equal_under_bijection':True,'graph_sha256':hashlib.sha256(raw).hexdigest(),
            'polygon_graph_sha256':hashlib.sha256((p/'polygon-graph.txt').read_bytes()).hexdigest()}
    (p/'graph-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
