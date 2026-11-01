# Release assets for v1.0.0

Attach `A7-k133-vertex.lrat.gz` and `A7-k133-vertex.lrat.gz.sha256`. The archive is 842,748,372 bytes and its SHA-256 is `874edda89e054b67e2b40dcb67e9e8a87c37ca6798e45b97756da110de6afe30`. It is the unchanged compressed binary LRAT required for the L134 replay. The historical restricted storage record remains in `data/lower/drive-manifest.json`.

The lightweight workflow does not replay LRAT. Download the release attachment anonymously, verify its size and SHA-256, and run the full replay with the pinned checker as described in VERIFY.md. Hosted CI and public download/replay are separate checks.
