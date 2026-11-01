# Minimum 144 under full C9 rotation invariance

This statement is restricted to matchings invariant under all rotations of the nine-gon. It is not an unrestricted lower bound.

The supplied 144-edge witness is a maximal matching and is fixed by all nine rotations, providing the upper bound in this restricted class.

Under C9 the 429 graph vertices form 49 orbits: 47 of size nine and two of size three. The checker reconstructs the action from the polygon diagonals and checks that it preserves all graph edges. For every edge it builds the full orbit. An invariant matching is a union of entire edge orbits; any orbit with repeated endpoints is unusable. Every usable orbit has nine edges and covers two complete size-nine vertex orbits. No usable orbit touches either size-three orbit, so those two must remain unmatched.

Maximality forces the neighboring orbits of those two mandatory-unmatched orbits to be covered. This leaves 43 size-nine orbits eligible to be unmatched. If an invariant matching had at most 135 edges, it would choose at most 15 usable edge orbits, cover at most 30 of the 47 size-nine vertex orbits, and leave at least 17 eligible orbits unmatched. Such unmatched orbits must be pairwise nonadjacent.

The certificate proves that no independent set of size 17 exists among those 43 eligible orbits. At a branch, it partitions possibilities into including or excluding a specified orbit. Inclusion removes that orbit and its neighbors and reduces the required size by one. At a leaf, it partitions the remaining candidate orbits into cliques. An independent set contains at most one vertex from each clique, so fewer cliques than the required number proves that leaf impossible. The checker verifies every branch, every exact partition, and every clique adjacency, without importing the search code or quotient-model builder.

The saved certificate has 281 nodes and 18,444 bytes, with SHA-256 `748dbd1c6eff9dd52c816916771688ae494681166d92215aa147c2b242e9b1e4`. The checker rejects removal of an eligible orbit, a changed target, and an invalid branch vertex.

Every invariant matching's size is a multiple of nine. Therefore a size below 144 would be at most 135, which was just excluded. Together with the witness this proves the restricted minimum is 144. The ordinary 143-edge witness shows that a globally optimal matching cannot have full C9 invariance, even though the global optimal value is still unresolved.

This finite certificate is checked with ordinary integer Python code. It is not an LRAT or Lean proof. Its checker was written in the same laboratory workflow; external independent review remains pending.
