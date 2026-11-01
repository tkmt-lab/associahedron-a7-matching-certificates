# Verification record

Prepared 2026-10-26; updated for version 1.0.0. This record describes the checks performed and their limits.

The existing laboratory record establishes upper witnesses 156, 144 and 143; the 143-edge witness was produced by Argon (Gemini). It records k=129…133 LRAT checks and a separate finite C9 certificate. This packet keeps the construction source and verification roles distinct. It does not adopt Argon's other symmetry classifications or speed measurements.

## Packet checks

The clean-copy replay passed on macOS ARM64 with Python 3.14.7. The packet verifier took 67.415 seconds; the entire bounded wrapper took 67.548 seconds, within the cumulative 600-second allowance. All three witnesses passed both matching checkers, the C9 certificate passed, the exact CNF was regenerated, and cake_lpr returned `s VERIFIED UNSAT` for k=133. Ten negative controls were rejected (six matching checks, three C9 mutations, one empty LRAT). The historical 143-edge candidate hash is now explicitly paired with both verifier outputs.

The packet's 2026-10-26 local replay is recorded in `verification/local.json`. The external preparation wrapper added `clean_copy_outside_development_cwd: true`; this is an observation by that wrapper, not a field emitted by `verify.py`. The historical receipt is retained unchanged. Its scope text predates the explicit LRAT suffix, and its matching negative controls used a repeated edge, a self-loop and an empty matching. The revised verifier replaces those with distinct edges sharing one endpoint, distinct nonadjacent vertices, and the 143-edge witness with one edge removed. It covers the two graph constructions, both matching checkers on each of the three witnesses, C9 invariance, the C9 finite certificate, corrupted-input controls, regeneration of the exact no-symmetry k=133 CNF, and, when `lrat_replayed` is true, the saved proof with cake_lpr. A passed receipt must name that exact layer; a quick run with `lrat_replayed=false` does not establish L134 by itself.

The full checker requires stdout exactly `s VERIFIED UNSAT` and successful exit, and rejects the empty-proof control. Local execution is bounded to a total of ten minutes for this preparation. The final elapsed time and platform are in the receipt. A same-author replay and a clean-copy run do not constitute independent review. The pinned GitHub Actions workflow is supplied but has not run on the hosted service.

## Drive preservation

The five accepted compressed LRAT files, totaling 1,203,708,299 bytes, were uploaded using the laboratory's dedicated Drive API authorization. Local SHA-256 values were matched to the accepted archive registry. After transfer, the API metadata for file ID, parent, name, size, MD5, and application provenance was reread, including a second read after all transfers. No full remote download was performed and no local original was removed.

The archive manifest records this exact verification scope. All five permission listings contained only the owner; public access was not enabled. A public download or release mirror is a release prerequisite, not a completed step. Auth credentials and transfer scripts are not part of this packet.

## Review and release evidence

- Independent review of the graph/encoding argument, witness checking, and restricted-symmetry proof; coordinated separately by the laboratory.
- Novelty comparison against primary sources, author data/code, and subsequent work. No worldwide novelty or optimality claim is certified here.
- The v1.0.0 release is intended to provide the archive as a GitHub release asset. Anonymous access and a downloaded-asset replay require separate verification.
- Hosted Linux CI results. Local macOS checks do not imply that hosted CI has run.

The unfinished k=134 and k=142 trials are not proof evidence. The last k=142 attempt did not complete all planned branches because its runner failed to start all threads. Neither those timeouts nor that technical failure support a nonexistence claim.
