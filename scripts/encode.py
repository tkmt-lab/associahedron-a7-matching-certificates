"""Independent ordered-tree/rotation graph and maximal-matching CNF."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json,math,hashlib,argparse
@lru_cache(None)
def trees(n):
 if n==0:return (None,)
 return tuple((a,b) for l in range(n) for a in trees(l) for b in trees(n-1-l))
def label(t):return '.' if t is None else '('+label(t[0])+label(t[1])+')'
def rotations(t):
 if t is None:return set()
 a,b=t;out=set()
 if a is not None:out.add((a[0],(a[1],b)))
 if b is not None:out.add(((a,b[0]),b[1]))
 out.update((x,b) for x in rotations(a));out.update((a,x) for x in rotations(b));return out
def triangulation(t):
 chords=[]
 def walk(a,start,root=False):
  if a is None:return start+1
  mid=walk(a[0],start);end=walk(a[1],mid)
  if not root:chords.append((start,end))
  return end
 walk(t,0,True);return tuple(sorted(chords))
def graph(n):
 ts=sorted(trees(n),key=label);idx={t:i for i,t in enumerate(ts)}
 edges=sorted({tuple(sorted((i,idx[r]))) for i,t in enumerate(ts) for r in rotations(t)})
 deg=[0]*len(ts)
 for u,v in edges:deg[u]+=1;deg[v]+=1
 assert len(ts)==math.comb(2*n,n)//(n+1) and set(deg)=={n-1}
 tris=list(map(triangulation,ts));assert len(set(tris))==len(ts)
 # Independent pairwise diagonal-intersection characterization of adjacency.
 flipped=[(i,j) for i,j in combinations(range(len(ts)),2) if len(set(tris[i])&set(tris[j]))==n-2]
 assert edges==flipped
 return {'n':n,'vertices':list(map(label,ts)),'triangulations':tris,'edges':edges}
class CNF:
 def __init__(self,n):self.n=n;self.clauses=[];self.counts={}
 def var(self):self.n+=1;return self.n
 def add(self,*lits):self.clauses.append(list(lits))
 def save(self,path):
  with Path(path).open('w') as f:
   f.write(f'p cnf {self.n} {len(self.clauses)}\n')
   for c in self.clauses:f.write(' '.join(map(str,c))+' 0\n')
def atmost(cnf,xs,k):
 """Forward truncated unary totalizer. All true thresholds forced upward."""
 if k<0:cnf.add();return
 if k>=len(xs):return
 cap=k+1
 def merge(xs):
  if len(xs)==1:return xs
  mid=len(xs)//2;a=merge(xs[:mid]);b=merge(xs[mid:]);o=[cnf.var() for _ in range(min(cap,len(a)+len(b)))]
  for i in range(len(a)+1):
   for j in range(len(b)+1):
    if 0<i+j<=len(o):cnf.add(*([-a[i-1]] if i else []),*([-b[j-1]] if j else []),o[i+j-1])
  return o
 out=merge(xs);cnf.add(-out[k])
def edge_permutations(g):
 n=g['n'];m=n+2;tri={tuple(map(tuple,t)):i for i,t in enumerate(g['triangulations'])};eidx={tuple(e):i+1 for i,e in enumerate(g['edges'])};perms=[]
 for s in [1,-1]:
  for r in range(m):
   vp=[]
   for t in g['triangulations']:
    tt=tuple(sorted(tuple(sorted(((s*a+r)%m,(s*b+r)%m))) for a,b in t));vp.append(tri[tt])
   ep=[eidx[tuple(sorted((vp[u],vp[v])))] for u,v in g['edges']]
   assert sorted(ep)==list(range(1,len(ep)+1))
   if ep!=list(range(1,len(ep)+1)):perms.append(ep)
 assert len(perms)==2*m-1 and len({tuple(x) for x in perms})==len(perms)
 return perms
def lex_leader(cnf,xs,ys):
 # p means all previous unequal-position pairs agree. Only forward implications
 # are needed; canonical equality-prefix values always extend a lex-min vector.
 p=None
 for x,y in zip(xs,ys):
  if x==y:continue
  prefix=[] if p is None else [-p]
  cnf.add(*prefix,-x,y)
  q=cnf.var();cnf.add(*prefix,-x,-y,q);cnf.add(*prefix,x,y,q);p=q

def encode(g,k,sym=False):
 edges=g['edges'];cnf=CNF(len(edges));inc=[[] for _ in g['vertices']]
 for i,(u,v) in enumerate(edges,1):inc[u].append(i);inc[v].append(i)
 for row in inc:
  for e,f in combinations(row,2):cnf.add(-e,-f)
 cnf.counts['matching']=len(cnf.clauses)
 for u,v in edges:cnf.add(*sorted(set(inc[u]+inc[v])))
 cnf.counts['maximal']=len(edges)
 before=len(cnf.clauses);atmost(cnf,list(range(1,len(edges)+1)),k);cnf.counts['cardinality']=len(cnf.clauses)-before
 before=len(cnf.clauses)
 if sym:
  for ep in edge_permutations(g):lex_leader(cnf,list(range(1,len(edges)+1)),ep)
 cnf.counts['symmetry']=len(cnf.clauses)-before
 return cnf

def validate_model(g,k,values):
 chosen=[(u,v) for i,(u,v) in enumerate(g['edges'],1) if values.get(i,False)];flat=[v for e in chosen for v in e]
 assert len(chosen)<=k and len(flat)==len(set(flat));covered=set(flat)
 assert all(u in covered or v in covered for u,v in g['edges'])
 return {'size':len(chosen),'edges':chosen,'vertices':[[g['vertices'][u],g['vertices'][v]] for u,v in chosen]}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--n',type=int,required=True);a.add_argument('--k',type=int,required=True);a.add_argument('--sym',action='store_true');a.add_argument('--out',required=True);args=a.parse_args();g=graph(args.n);c=encode(g,args.k,args.sym);c.save(args.out);print(json.dumps({'vertices':len(g['vertices']),'edges':len(g['edges']),'variables':c.n,'clauses':len(c.clauses),'blocks':c.counts}))
