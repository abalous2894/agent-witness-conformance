# Agent Witness Conformance (AWC)

Deterministic conformance profiles for **agent / MCP session evidence exports**: a reference trace vs an exported bundle, with adversarial fixtures and a **non-LLM** grader pipeline.

AWC v0.1 is intentionally narrow: **witness integrity** only (hop set, bindings, completeness claims). It normatively reuses the wire formats from [WitnessDiff](https://github.com/abalous2894/witnessdiff) 1.x — no parallel `awc.*` export schema in v0.1.

## Skeptic walkthrough (≈2 minutes)

```bash
git clone https://github.com/abalous2894/agent-witness-conformance.git
cd agent-witness-conformance
python -m venv .venv && source .venv/bin/activate
pip install git+https://github.com/abalous2894/witnessdiff.git@v1.0.0
pip install -e ".[dev]"
awc run-profile awc-v0.1
```

Exit code `0` means all **15** profile cases match their expected verdicts.

Single pair:

```bash
awc verify -r fixtures/profiles/awc-v0.1/cases/awc-002-silent-omission/reference.json \
           -e fixtures/profiles/awc-v0.1/cases/awc-002-silent-omission/evidence.json
```

## Architecture (v0.1)

| Layer | Responsibility |
|-------|----------------|
| **Wire format** | `witnessdiff.reference-trace/v1`, `witnessdiff.evidence-bundle/v1` ([JSON Schema](spec/schemas/)) |
| **AWC preflight** | Structural rules → `INVALID_INPUT` (e.g. duplicate `action_id`) |
| **Reference comparator** | `witnessdiff.compare_witness_integrity` (deterministic hop witness) |
| **Profile** | `spec/awc-profile-v0.1.json` + `fixtures/profiles/awc-v0.1/manifest.json` |

Implementors claim **AWC v0.1 export conformance** when their exporter produces bundles that pass the profile when graded against the suite’s reference traces. The open-source **reference grader** is this repository’s `awc` CLI.

## Documentation

- [SPEC.md](SPEC.md) — normative profile summary  
- [CLAIM-BOUNDARY.md](CLAIM-BOUNDARY.md) — what AWC does *not* prove  
- [THREAT-MODEL.md](THREAT-MODEL.md) — exporter failure modes covered by fixtures  
- [docs/SKEPTIC-WALKTHROUGH.md](docs/SKEPTIC-WALKTHROUGH.md) — extended review guide  

## Relationship to WitnessDiff

- **WitnessDiff** — productized regression runner, API, behavioral lane, viewer.  
- **AWC** — portable **conformance profile + vectors** for third-party “does your export lie about completeness?” reviews.

## License

Apache-2.0 — see [LICENSE](LICENSE).
