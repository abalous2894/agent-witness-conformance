# AWC v0.1 — Normative summary

**Profile id:** `awc-v0.1`  
**Machine-readable:** [spec/awc-profile-v0.1.json](spec/awc-profile-v0.1.json)

## 1. Scope

AWC v0.1 defines a **deterministic grading pipeline** for pairs:

1. **Reference trace** — instrumented ground truth *for the test* (`witnessdiff.reference-trace/v1`).  
2. **Evidence bundle** — exporter output (`witnessdiff.evidence-bundle/v1`).

Grading produces a **verdict** from [spec/awc-verdicts-v0.1.json](spec/awc-verdicts-v0.1.json).

## 2. Wire format (fact-checked)

AWC v0.1 **does not** introduce alternate schema constants. Documents MUST use:

| Role | `schema` field value |
|------|----------------------|
| Reference | `witnessdiff.reference-trace/v1` |
| Evidence | `witnessdiff.evidence-bundle/v1` |

JSON Schemas in `spec/schemas/` are copies aligned with WitnessDiff 1.0 fixture schemas.

## 3. Grader pipeline (normative order)

1. **Parse** both documents; parse failures → `INVALID_INPUT`.  
2. **AWC preflight v0.1** ([src/awc/preflight.py](src/awc/preflight.py)):  
   - Duplicate `action_id` within reference or evidence → `INVALID_INPUT`.  
3. **WitnessDiff comparator** `compare_witness_integrity` — verdict mapping per WitnessDiff methodology.

Session id mismatch is handled by the WitnessDiff comparator (`INVALID_INPUT`).

## 4. Conformance

- **Reference grader conformance:** `awc run-profile awc-v0.1` exits 0 on the published fixture manifest.  
- **Exporter conformance (informative):** vendor publishes bundles that grade as expected against their own reference traces *and* passes AWC negative vectors when replayed in customer tests.

## 5. Non-goals (v0.1)

See [CLAIM-BOUNDARY.md](CLAIM-BOUNDARY.md).
