"""Continuous evaluation CLI.

Runs the full arena against the golden dataset (data/evals/cases.jsonl) and
reports:
  - hit rate on expected_winner (when set)
  - confidence band match (expected_confidence is a list of acceptable values)
  - must_mention coverage in the final architecture
  - citation validity per agent
  - run-to-run variance (re-runs the same case N times and checks the winner
    stays the same — should be 100% with seed=42)

Usage:
    python eval.py                       # all cases, 1 run each
    python eval.py --case bank_rag_eu    # one case
    python eval.py --variance 3          # variance check: 3 runs per case
    python eval.py --out report.md       # write a markdown report
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

from agent_arena.arena import run_agent_arena_with_llm_planner_pydantic_async
from agent_arena.config import DEFAULT_MODEL
from agent_arena.schemas import DEFAULT_BUSINESS_CONTEXT


CASES_PATH = BASE / "data" / "evals" / "cases.jsonl"


def load_cases() -> list[dict]:
    return [json.loads(line) for line in CASES_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


async def run_one_case(case: dict, model: str) -> dict:
    result = await run_agent_arena_with_llm_planner_pydantic_async(
        user_idea=case["idea"],
        model=model,
        business_context=DEFAULT_BUSINESS_CONTEXT,
        client_id=f"eval-{case['id']}",
    )
    v = result.verdict
    winner = v.winner if v else None
    confidence = v.confidence if v else None
    proposal_lower = (result.final_architecture_proposal or "").lower()
    mentions = {kw: kw.lower() in proposal_lower for kw in case.get("must_mention", [])}

    expected_winner = case.get("expected_winner")
    expected_conf = set(case.get("expected_confidence", []))

    winner_ok = (expected_winner is None) or (winner == expected_winner)
    confidence_ok = (not expected_conf) or (confidence in expected_conf)
    mentions_ok = all(mentions.values()) if mentions else True

    return {
        "case_id": case["id"],
        "winner": winner,
        "expected_winner": expected_winner,
        "winner_ok": winner_ok,
        "confidence": confidence,
        "expected_confidence": list(expected_conf),
        "confidence_ok": confidence_ok,
        "mentions": mentions,
        "mentions_ok": mentions_ok,
        "azure_valid": result.azure_validation.valid,
        "aws_valid": result.aws_validation.valid,
        "gcp_valid": result.gcp_validation.valid if result.gcp_validation else None,
        "rewrites": result.rewrite_counts,
        "specialist_count": len(result.specialist_findings or []),
        "run_id": result.run_id,
    }


async def main_async(args):
    cases = load_cases()
    if args.case:
        cases = [c for c in cases if c["id"] == args.case]
        if not cases:
            print(f"Case '{args.case}' not found.")
            return 1

    model = os.getenv("AGENT_ARENA_MODEL", DEFAULT_MODEL)
    print(f"Running {len(cases)} case(s) x {args.variance} run(s) on model {model}...\n")

    per_case_results: dict[str, list[dict]] = {}
    for case in cases:
        per_case_results[case["id"]] = []
        for i in range(args.variance):
            print(f"  [{case['id']}] run {i+1}/{args.variance}...", flush=True)
            try:
                r = await run_one_case(case, model)
            except Exception as exc:
                r = {"case_id": case["id"], "error": str(exc)}
            per_case_results[case["id"]].append(r)

    # Aggregate
    total_runs = sum(len(rs) for rs in per_case_results.values())
    winner_hits = sum(1 for rs in per_case_results.values() for r in rs if r.get("winner_ok"))
    conf_hits   = sum(1 for rs in per_case_results.values() for r in rs if r.get("confidence_ok"))
    ment_hits   = sum(1 for rs in per_case_results.values() for r in rs if r.get("mentions_ok"))
    valid_runs  = sum(
        1 for rs in per_case_results.values() for r in rs
        if r.get("azure_valid") and r.get("aws_valid") and r.get("gcp_valid") in (True, None)
    )

    variance_consistent = 0
    for rs in per_case_results.values():
        winners = [r.get("winner") for r in rs if not r.get("error")]
        if len(set(winners)) <= 1 and winners:
            variance_consistent += 1

    summary = {
        "total_cases": len(cases),
        "runs_per_case": args.variance,
        "total_runs": total_runs,
        "winner_hit_rate": f"{winner_hits}/{total_runs}",
        "confidence_hit_rate": f"{conf_hits}/{total_runs}",
        "must_mention_hit_rate": f"{ment_hits}/{total_runs}",
        "all_citations_valid": f"{valid_runs}/{total_runs}",
        "variance_consistent_cases": f"{variance_consistent}/{len(cases)}",
    }

    print("\n=== SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    if args.out:
        report = _render_report(summary, per_case_results)
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"\nReport written to {args.out}")

    return 0


def _render_report(summary: dict, per_case: dict) -> str:
    lines = ["# Eval report", "", "## Summary", ""]
    for k, v in summary.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("\n## Per-case detail\n")
    for case_id, runs in per_case.items():
        lines.append(f"### {case_id}")
        for i, r in enumerate(runs, 1):
            if "error" in r:
                lines.append(f"- Run {i}: ERROR — {r['error']}")
                continue
            badges = []
            badges.append("✅" if r.get("winner_ok") else "❌")
            badges.append("✅" if r.get("confidence_ok") else "❌")
            badges.append("✅" if r.get("mentions_ok") else "❌")
            lines.append(
                f"- Run {i}: winner={r.get('winner')} (esperado {r.get('expected_winner')}) "
                f"· confidence={r.get('confidence')} {' '.join(badges)} "
                f"· run_id={r.get('run_id')}"
            )
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", help="Run only this case id.")
    parser.add_argument("--variance", type=int, default=1, help="Re-runs per case (for variance check).")
    parser.add_argument("--out", help="Path to write a markdown report.")
    args = parser.parse_args()
    sys.exit(asyncio.run(main_async(args)))
