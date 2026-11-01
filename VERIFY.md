# Verification instructions

Run all commands from the packet root. Python 3.11+ and `c++` with C++17 support suffice for `python3 -B verify.py`. No Python packages, network connection, GPU, or SAT solver are needed for the small checks. The GitHub Actions workflow is configured to perform these same checks on Ubuntu; it does not automatically access the restricted Drive archive or replay LRAT.

## Full lower-bound replay

The optional checker is [cake_lpr](https://github.com/tanyongkiam/cake_lpr), pinned to commit `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa`. Build in a separate directory:

```sh
git clone https://github.com/tanyongkiam/cake_lpr.git cake-lpr-tools
git -C cake-lpr-tools checkout a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
make -C cake-lpr-tools
```

On macOS/ARM64 use `make -C cake-lpr-tools cake_lpr_arm8` instead and pass the resulting `cake_lpr` executable (the ARM target also writes this filename). These are the upstream build targets; we did not rerun the Linux build in this preparation. See [DEPENDENCIES.json](DEPENDENCIES.json) for source and historical binary identities.

Obtain `A7-k133-vertex.lrat.gz` from the version 1.0.0 release attachment linked in README. Keep it outside the tracked repository. Then run:

```sh
python3 -B verify.py --lrat /path/to/A7-k133-vertex.lrat.gz \
  --checker /path/to/cake_lpr --output verification/my-full-check.json
```

The wrapper regenerates the exact CNF, checks compressed size and SHA-256, decompresses into its temporary directory, checks raw size and SHA-256, and calls:

```sh
cake_lpr --CML_HEAP_SIZE=1536 --CML_STACK_SIZE=128 A7-k133.cnf proof.lrat
```

The pinned cake_lpr executable reads the saved CaDiCaL binary LRAT directly; no format conversion is needed.

It requires exit code 0 **and stdout exactly `s VERIFIED UNSAT`** after stripping surrounding whitespace. An empty proof can fail with exit code 0, so exit code alone is not sufficient. An empty-proof negative control is included in full mode. Temporary decompressed data is removed when the check exits. No proof is generated and no solver is run.

The 540-second default budget can be changed with `--budget-seconds` up to 600 seconds. A timeout means the check did not finish under that cap, not that the certificate is invalid. The packet preparation's actual local result is in `verification/local.json`; it is distinct from hosted CI, which has not been run before publication.

## Inspect individual witnesses and the C9 certificate

```sh
python3 -B scripts/check_matching.py data/graph.json data/matchings/matching-143.json
c++ -O2 -std=c++17 scripts/check_matching.cpp -o /tmp/a7-matching-check
/tmp/a7-matching-check data/polygon-graph.txt data/matchings/matching-143.txt
python3 -B scripts/check_c9_certificate.py
```

Repeat the matching commands with 144 or 156 for the other witnesses. `verify.py` checks all three, their text/JSON consistency, all nine rotation images of the 144-edge witness, and agreement of graph construction methods. Individual checkers assume their supplied graph; the wrapper also verifies graph regeneration. Do not disable Python assertions.
