from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from witnessdiff.claim_parser import load_evidence_bundle
from witnessdiff.comparators import compare_witness_integrity
from witnessdiff.models import ComparisonReport, EvidenceBundle, ReferenceTrace, WitnessVerdict
from witnessdiff.trace_parser import load_reference_trace

from awc.preflight import invalid_input_verdict_note, run_awc_preflight


def _report_to_expected_shape(report: ComparisonReport) -> dict[str, Any]:
    return {
        "schema": "witnessdiff.comparison-report/v1",
        "session_id": report.session_id,
        "ok": report.ok,
        "verdict": report.verdict.value,
        "reference_action_count": report.reference_action_count,
        "evidence_action_count": report.evidence_action_count,
        "completeness_claim": report.completeness_claim,
    }


def _invalid_input_report(
    *,
    session_id: str,
    reference_action_count: int,
    evidence_action_count: int,
    completeness_claim: str,
    note: str,
) -> ComparisonReport:
    return ComparisonReport(
        session_id=session_id,
        ok=False,
        verdict=WitnessVerdict.INVALID_INPUT,
        reference_action_count=reference_action_count,
        evidence_action_count=evidence_action_count,
        completeness_claim=completeness_claim,
        findings=[],
        note=note,
    )


def grade_witness_pair(
    reference: ReferenceTrace,
    evidence: EvidenceBundle,
) -> ComparisonReport:
    """AWC v0.1 grader: preflight → WitnessDiff reference comparator."""
    violation = run_awc_preflight(reference, evidence)
    if violation:
        return _invalid_input_report(
            session_id=reference.session_id,
            reference_action_count=len(reference.actions),
            evidence_action_count=len(evidence.actions),
            completeness_claim=evidence.completeness_claim,
            note=invalid_input_verdict_note(violation),
        )
    return compare_witness_integrity(reference, evidence)


def grade_paths(reference_path: Path, evidence_path: Path) -> ComparisonReport:
    try:
        reference = load_reference_trace(reference_path)
        evidence = load_evidence_bundle(evidence_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return _invalid_input_report(
            session_id="unknown",
            reference_action_count=0,
            evidence_action_count=0,
            completeness_claim="unknown",
            note=f"parse error: {exc}",
        )
    return grade_witness_pair(reference, evidence)


def assert_matches_expected(report: ComparisonReport, expected: dict[str, Any]) -> list[str]:
    actual = _report_to_expected_shape(report)
    errors: list[str] = []
    for field in (
        "ok",
        "verdict",
        "reference_action_count",
        "evidence_action_count",
        "completeness_claim",
        "session_id",
    ):
        exp = expected.get(field)
        if exp is None:
            continue
        got = actual.get(field)
        if got != exp and str(got) != str(exp):
            errors.append(f"{field}: expected {exp!r}, got {got!r}")
    return errors
