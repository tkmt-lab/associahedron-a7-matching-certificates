"""Redundant covered-vertex constraints, preserving the original edge encoding."""
from encode import encode,atmost

def strengthened(g,k,sym=False):
 c=encode(g,k,sym);edges=g['edges'];inc=[[] for _ in g['vertices']]
 for i,(u,v) in enumerate(edges,1):inc[u].append(i);inc[v].append(i)
 ys=[c.var() for _ in inc];before=len(c.clauses)
 for y,row in zip(ys,inc):
  for x in row:c.add(-x,y)
  c.add(-y,*row)
 for u,v in edges:c.add(ys[u],ys[v])
 atmost(c,ys,2*k)
 c.counts['redundant_covered_vertex']=len(c.clauses)-before
 return c
