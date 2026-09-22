from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from awc.grader import grade_paths
from awc.profile import load_profile
from awc.runner import run_profile

app = typer.Typer(
    name="awc",
    help="Agent Witness Conformance — deterministic session-export oracles.",
    no_args_is_help=True,
)
console = Console()


@app.command("verify")
def verify_cmd(
    reference: Path = typer.Option(..., "--reference", "-r", help="Reference trace JSON"),
    evidence: Path = typer.Option(..., "--evidence", "-e", help="Evidence bundle JSON"),
) -> None:
    """Grade one reference/evidence pair (AWC v0.1 grader)."""
    report = grade_paths(reference, evidence)
    console.print(f"verdict={report.verdict.value} ok={report.ok}")
    if report.note:
        console.print(report.note)
    if not report.ok:
        raise typer.Exit(code=1)


@app.command("run-profile")
def run_profile_cmd(
    profile_id: str = typer.Argument("awc-v0.1", help="Profile id (e.g. awc-v0.1)"),
) -> None:
    """Run all cases for a conformance profile."""
    result = run_profile(profile_id)
    table = Table(title=f"Profile {result.profile_id}")
    table.add_column("case")
    table.add_column("verdict")
    table.add_column("status")
    for case in result.cases:
        status = "PASS" if case.passed else "FAIL"
        table.add_row(case.case_id, case.actual_verdict or "-", status)
    console.print(table)
    console.print(f"passed={result.passed} failed={result.failed}")
    if result.failed:
        for case in result.cases:
            for err in case.errors:
                console.print(f"[red]{case.case_id}[/red]: {err}")
        raise typer.Exit(code=1)


@app.command("explain")
def explain_cmd(
    case_id: str = typer.Argument(..., help="Case id under fixtures/profiles/<profile>/cases/"),
    profile_id: str = typer.Option("awc-v0.1", "--profile", "-p"),
) -> None:
    """Print paths and expected verdict for a profile case."""
    profile = load_profile(profile_id)
    match = next((c for c in profile.cases if c.case_id == case_id), None)
    if not match:
        typer.echo(f"unknown case: {case_id}", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"reference: {match.reference_path}")
    typer.echo(f"evidence:  {match.evidence_path}")
    typer.echo(f"expected:  {match.expected_path}")
    case_md = match.directory / "CASE.md"
    if case_md.is_file():
        typer.echo("\n" + case_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    app()
