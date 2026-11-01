# Maximal matchings in the associahedron A7: witnesses and certificates

This data-and-tools package records **134 ≤ M(A7) ≤ 143**, where M is the minimum number of edges in a maximal matching. The exact value is unresolved. Among maximal matchings invariant under all nine rotations of the polygon, the minimum is **144**. Thus a smallest unrestricted maximal matching cannot preserve that full rotation symmetry.

**Version 1.0.0.** This package provides the saved evidence and verification tools. Independent external review and novelty comparison are not claimed.

## The object and the evidence

A7 has 429 vertices and 1287 edges and is 6-regular. Its vertices are ordered full binary trees with seven internal nodes; adjacency is one tree rotation. A second construction uses triangulations of a convex nine-gon and diagonal flips. Vertex IDs are the lexicographic order of the tree strings in `data/graph.json`; `.` denotes a leaf and `(left right)` an internal node, without the space.

A matching has no repeated endpoint. It is maximal if no further edge can be added, equivalently if its unmatched vertices form an independent set. A minimum maximal matching is not a maximum-cardinality matching.

| ID | Statement | Evidence and verification |
|---|---|---|
| U143 | There exists a maximal matching with 143 edges | `data/matchings/matching-143.{txt,json}`, checked by Python and C++ implementations |
| U144 | There exists a C9-invariant maximal matching with 144 edges | The 144-edge files, both matching checkers, and all nine rotation images |
| U156 | There exists a maximal matching with 156 edges | The 156-edge files and both matching checkers; retained as a historical construction |
| L134 | No maximal matching has at most 133 edges | `data/lower/A7-k133.cnf`, its externally stored binary LRAT certificate, and cake_lpr; the graph/CNF correspondence is explained separately |
| C9MIN | Within C9-invariant maximal matchings, 144 is the minimum | U144 plus `data/c9/c9-no17-certificate.json` and its search-free finite checker |

[claims.json](claims.json) gives the scope, evidence, and non-claims in a machine-readable list. [VERIFICATION-RECORD.md](VERIFICATION-RECORD.md) distinguishes existing evidence, this packet's checks, and review still needed. The full local replay, including LRAT, passed in 67.5 seconds; this is a local measurement, not a hosted-CI or cross-platform result.

The 143-edge construction was produced by **Argon (Gemini)** and checked using the laboratory's verifiers. The laboratory produced the 156-edge and 144-edge constructions; the latter used Argon's earlier 153-edge C9 example and orbit-based idea. AI systems are tools, not authors. The provenance and roles are recorded in [PROVENANCE.json](PROVENANCE.json) and [SOURCES.md](SOURCES.md).

## Verify the small packet

Requirements: Python 3.11 or later and a C++17 compiler available as `c++`. Only the Python standard library is used. From this directory:

```sh
python3 -B verify.py
```

This regenerates the two graph representations, checks all three matching witnesses with both implementations, checks C9 invariance and the finite C9 certificate, and regenerates the k=133 CNF byte-for-byte. It also checks rejection of two different edges sharing one endpoint, a pair of distinct nonadjacent vertices, a 143-edge witness with one edge removed, and corrupted C9 inputs. It does **not** run a SAT solver or replay the large LRAT proof. A successful lightweight CI run alone does not certify L134.

Assertions are part of the checking code: do not use `python -O`. Work files are placed in `.cache/`. The packet manifest checks saved bytes but is not a digital signature or a substitute for mathematical verification.

## The large lower-bound certificate

The one certificate needed for L134 is:

| Item | Value |
|---|---|
| Archive | `A7-k133-vertex.lrat.gz` |
| Release asset | [Download k=133 proof](https://github.com/tkmt-lab/associahedron-a7-matching-certificates/releases/download/v1.0.0/A7-k133-vertex.lrat.gz) |
| SHA-256 sidecar | [Download SHA-256](https://github.com/tkmt-lab/associahedron-a7-matching-certificates/releases/download/v1.0.0/A7-k133-vertex.lrat.gz.sha256) |
| Compressed bytes | 842,748,372 |
| Compressed SHA-256 | `874edda89e054b67e2b40dcb67e9e8a87c37ca6798e45b97756da110de6afe30` |
| Decompressed bytes | 1,999,785,977 |
| Decompressed SHA-256 | `5dfc84aab0728db05153915ab557bb7d2a6efe4dfa26c3e8c4b38b7be5b2521b` |
| CNF SHA-256 | `287cc482b528d49e57d5b34c787b1e72e8092f73059ee7b410c79995f62aefb6` |

The unchanged k=133 archive is supplied as a release asset. The historical restricted Drive storage record is retained in [drive-manifest.json](data/lower/drive-manifest.json). The other four archived proofs are historical records and their CNFs are not included in this package. See [RELEASE-ASSETS.md](RELEASE-ASSETS.md) for the manifest and validation steps.

Download the k=133 archive when access is available, build the pinned cake_lpr version, and run (the build and full replay have been checked on macOS ARM64 only; Linux remains untested):

```sh
python3 -B verify.py \
  --lrat /path/to/A7-k133-vertex.lrat.gz \
  --checker /path/to/cake_lpr \
  --output verification/my-full-check.json
```

[VERIFY.md](VERIFY.md) contains build instructions and the exact success criterion. Allow about 2 GB RAM and at least 3.5 GB free disk for the archive, decompressed proof and packet. The default wall-time budget is 540 seconds; elapsed time depends on hardware. The repository does not promise a ten-minute run on every machine.

## What this is useful for

Researchers in graph associahedra, edge domination, and exact combinatorial optimization can reuse the fixed graph, compare witness construction methods, and check the symmetry-restricted evidence. They can independently replay the saved lower-bound evidence as well. Producing a new matching and checking it are separate operations; no search program is needed to check the three supplied witnesses.

The package does not establish M(A7)=143, a general Catalan-number formula, a new best bound in the entire literature, or a hardware speedup. Q1, M(A_n)=ceil(C_n/3), n≥2, is a conjecture stated by this package, motivated by the cited small values and the 143-edge witness. We do not attribute this equality to Brenner et al. or claim priority for it. Timeouts and an incomplete k=142 run are not lower-bound evidence. C9MIN is not a lower bound of 144 for unrestricted matchings.

## Mathematical and software boundaries

A successful cake_lpr run certifies the supplied CNF's unsatisfiability. [ENCODING.md](docs/ENCODING.md) supplies the graph-to-CNF argument and describes checks made on small examples; that correspondence has not been formalized in a proof assistant. The C9 result uses a finite integer certificate and an ordinary Python checker, not a Lean or LRAT formalization. The two matching checkers were written within the same laboratory workflow and do not constitute external independent review.

The comparison baseline comes from Brenner, Fink, Hoang, Merino and Pilaud, *Minimum Maximal Matchings in Permutahedra*, Remark 7/Table 1, and a general regular-graph bound of Baste et al. These general bounds give 129 ≤ M(A7) ≤ 210; this packet records 134 ≤ M(A7) ≤ 143. This comparison does not assert the best prior bounds in the literature. See [SOURCES.md](SOURCES.md). We thank these authors and the CaDiCaL and cake_lpr developers for the problem, methods, and checking infrastructure on which this work relies.

Project-owned code is Apache-2.0; original documentation and generated witness/certificate data are CC-BY-4.0. See [LICENSE](LICENSE) and [CITATION.cff](CITATION.cff). Third-party implementations and papers are not bundled or relicensed.
