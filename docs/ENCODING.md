# Graph-to-CNF correspondence for L134

This is a mathematical explanation and a record of finite checks, not a proof-assistant formalization.

## The graph

Ordered full binary trees with n internal nodes are enumerated recursively by choosing the size of the left subtree and pairing every left and right tree. Their labels use `.` for a leaf and `(left right)` for an internal node, without spaces. At every subtree, `((a,b),c)` and `(a,(b,c))` are related by a rotation. These unordered pairs are the graph edges; labels are sorted before vertex IDs are assigned.

Each non-root internal subtree spans a consecutive interval [a,b) of leaves and maps to the diagonal (a,b) of a convex (n+2)-gon. This gives n−1 diagonals. For A7, `graph_models.py` independently enumerates polygon triangulations by diagonal flips and checks the bijection and equality of the two edge sets. `encode.py` separately reconstructs tree rotations and checks adjacency by sharing n−2 diagonals. The saved graph has 429 vertices, 1287 edges and degree 6.

## Edge variables and maximality

For every graph edge e, x_e says that e is chosen. The clauses are:

1. For any two distinct edges incident to one vertex, `not x_e or not x_f`.
2. For each edge uv, a positive disjunction of all chosen-edge variables incident to u or v.
3. A cardinality encoding requiring at most k chosen edges.

The first condition is exactly the matching condition. The second is equivalent to maximality: an edge with both endpoints unmatched could be added; conversely, if each edge touches a matched endpoint, no edge can be added to the matching.

The cardinality encoding is a forward, truncated unary totalizer. Each output threshold t_j denotes that its subtree contains at least j true inputs; thresholds are retained up to k+1. Every pair of left/right thresholds forces the corresponding sum threshold, with threshold zero treated as true. The root's (k+1)-th threshold is forbidden. By induction, actual true inputs force every required threshold, so k+1 true edge variables are impossible. Conversely, with at most k true inputs, setting every auxiliary variable to its actual threshold satisfies every implication. Thus omitting reverse implications does not change the allowed edge assignments.

## Redundant covered-vertex variables

The adopted k=133 CNF also has y_v equivalent to the disjunction of edge variables incident to v. It contains `not x_e or y_v` for every incident edge and `not y_v or OR(x_e)` for the reverse implication. It adds `y_u or y_v` for each graph edge uv and a second totalizer enforcing at most 2k true y variables.

A matching covers exactly twice as many vertices as its number of edges, so the latter cardinality condition follows from the edge bound. The positive covered-vertex clauses follow from maximality. These additions cannot remove a valid matching and cannot introduce one. No outside lower-bound theorem is inserted as a clause.

Therefore the adopted CNF is satisfiable if and only if A7 has a maximal matching of at most 133 edges. **No symmetry breaking is used in this adopted CNF.** The saved instance has 15,590 variables and 268,066 clauses. The packet regenerates it and requires SHA-256 `287cc482b528d49e57d5b34c787b1e72e8092f73059ee7b410c79995f62aefb6`.

## What was checked and what remains

Before this packet was prepared, the implementation was checked on A3–A5 at the known boundaries 2,5,14, with SAT witnesses checked directly and UNSAT cases checked via LRAT. A3/A4 were also compared with exhaustive matching enumeration, and the totalizer was checked on 768 small assignments by a separate small DPLL implementation. These are historical implementation checks, not rerun by the packet and not a substitute for the correspondence argument.

The full packet replay checks the saved k=133 LRAT with cake_lpr. Since that CNF expresses a bound of at most 133, its UNSAT result excludes all smaller sizes as well and gives M(A7)≥134. The input model and encoding remain part of the trusted mathematical correspondence; we do not claim end-to-end formal verification of the original combinatorial theorem.
