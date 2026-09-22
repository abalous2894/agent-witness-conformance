from __future__ import annotations

from witnessdiff.models import EvidenceBundle, ReferenceTrace


def duplicate_action_ids(actions: list) -> list[str]:
    """Return action_id values that appear more than once (AWC v0.1 §4.2)."""
    seen: set[str] = set()
    duplicates: set[str] = set()
    for action in actions:
        aid = getattr(action, "action_id", None)
        if not aid:
            continue
        if aid in seen:
            duplicates.add(aid)
        seen.add(aid)
    return sorted(duplicates)


def run_awc_preflight(
    reference: ReferenceTrace,
    evidence: EvidenceBundle,
) -> str | None:
    """
    AWC-specific structural rules not covered by WitnessDiff compare.

    Returns human-readable violation text, or None if preflight passes.
    """
    ref_dupes = duplicate_action_ids(reference.actions)
    if ref_dupes:
        return (
            "reference trace contains duplicate action_id value(s): "
            + ", ".join(ref_dupes[:3])
            + (" …" if len(ref_dupes) > 3 else "")
        )

    ev_dupes = duplicate_action_ids(evidence.actions)
    if ev_dupes:
        return (
            "evidence bundle contains duplicate action_id value(s): "
            + ", ".join(ev_dupes[:3])
            + (" …" if len(ev_dupes) > 3 else "")
        )

    return None


def invalid_input_verdict_note(reason: str) -> str:
    return reason
