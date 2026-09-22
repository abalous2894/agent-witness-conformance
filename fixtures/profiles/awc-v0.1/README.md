# AWC v0.1 fixtures

Each case directory contains:

- `reference.json` — `witnessdiff.reference-trace/v1`
- `evidence.json` — `witnessdiff.evidence-bundle/v1`
- `expected.json` — subset of `witnessdiff.comparison-report/v1` fields used by `awc run-profile`
- `CASE.md` — optional narrative (required for AWC-only rules)

Cases `awc-001`–`awc-010` and `awc-014` are ported from [WitnessDiff](https://github.com/abalous2894/witnessdiff) evidence fixtures (same semantics, independent paths for stable profile ids).
