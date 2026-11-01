# Sources and attribution

## Mathematical references

- Sofia Brenner, Jiří Fink, Hung P. Hoang, Arturo Merino, Vincent Pilaud. *Minimum Maximal Matchings in Permutahedra*. Electronic Journal of Combinatorics 33(2), P2.50 (2026). [DOI](https://doi.org/10.37236/14145), [published text](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i2p50/pdf/). Remark 7 (pp.4–5), applying Proposition 4, gives the associahedron lower bound `ceil((n-1) C_n / (3n-1))`, where `C_n = binom(2n,n)/(n+1)`. At n=7 this is `ceil(6 × 429 / 20) = 129`. This evaluates a general bound, not an extrapolation from the table. Table 1 lists minimum maximal-matching sizes 1,2,5,14,44 for n=2,…,6. We make no claim that n=7 is unstudied elsewhere.
- Julien Baste, Maximilian Fürst, Michael A. Henning, Elena Mohr, Dieter Rautenbach. *Bounding and approximating minimum maximal matchings in regular graphs*. Discrete Mathematics 344(3), 112243 (2021), [DOI](https://doi.org/10.1016/j.disc.2020.112243); preprint [arXiv:1905.12241v1](https://arxiv.org/abs/1905.12241v1) (2019). Theorem 2, equation (2), p.2 **of the preprint** gives `gamma_e(G) <= [Delta(2Delta-3)N + 2Delta] / [2(Delta-1)(2Delta-1)]` for connected Delta-regular graphs with Delta≥3. Substitution N=429, Delta=6, and integrality give `floor(23178/110) = 210`. The publisher's bibliographic record was checked; the journal theorem numbering was not verified. This is a reference baseline, not a claim to the best previously known A7 bound.

Our n counts internal tree nodes, as in Remark 7/Table 1. We write A_n for this graph: it has C_n vertices and also represents triangulations of a convex (n+2)-gon. Thus A7 here corresponds to their n=7 convention, not a seven-dimensional polytope.

Q1, `M(A_n)=ceil(C_n/3)` for n≥2, is a conjecture stated by this package, motivated by those literature values and the 143-edge witness. We do not attribute this equality to Brenner et al.: their associahedron discussion and open questions do not state it. This is not a claim of priority for the conjecture. The tabulated small values remain prior results. Independent novelty review is pending; this source comparison does not establish novelty.

## Computational dependencies

- [CaDiCaL](https://github.com/arminbiere/cadical), version 3.0.1, source commit `c60730422e758ef1cebe7aeddf2dda31c996bf04`: historical SAT and binary-LRAT producer. It is not required to replay the saved evidence.
- [cake_lpr](https://github.com/tanyongkiam/cake_lpr), source commit `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa`: external checker for the saved LRAT proof, based on CakeML. We rely on its explicit verification result and record the executable hash. Its assurances do not formalize our graph construction or encoding argument.

The software papers are:

- Armin Biere, Tobias Faller, Katalin Fazekas, Mathias Fleury, Nils Froleyks, Florian Pollitt. *CaDiCaL 2.0*. CAV 2024, LNCS 14681, pp.133–152. [DOI](https://doi.org/10.1007/978-3-031-65627-9_7). This is the [citation requested by the developers](https://github.com/arminbiere/cadical); the historical producer here is the separately pinned version 3.0.1 above.
- Yong Kiam Tan, Marijn J. H. Heule, Magnus O. Myreen. *cake_lpr: Verified Propagation Redundancy Checking in CakeML*. TACAS 2021, LNCS 12652, pp.223–241. [DOI](https://doi.org/10.1007/978-3-030-72013-1_12), [open text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7984575/). The paper describes the checker and its verification; the exact executable used here is identified separately above and in the replay receipt.

## Construction and checking roles

Argon (Gemini) produced the 143-edge construction. The laboratory checked it with its Python/tree and C++/polygon matching checkers; the packet replay records both outputs and the exact candidate hashes. Argon's other timings or symmetry classifications are not adopted as claims here.

The laboratory produced the 156-edge construction, the 144-edge C9 construction, the CNF/LRAT lower-bound evidence, and the C9 finite certificate. The 144-edge work used Argon's earlier 153-edge example and orbit-based suggestion. Codex assisted with implementation, computation, documentation, and checks; Claude coordinated and performed additional checks. Those roles are distinct from the independent review still pending. Tatsuhiko Takimoto is the human author; AI systems are acknowledged as tools.

`PROVENANCE.json` records source paths, fixed commits, and hashes. Mathematical verification uses the supplied files and does not require access to the laboratory's development repository.
