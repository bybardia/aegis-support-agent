import argparse
import json
import pandas as pd
from rich.console import Console
from rich.panel import Panel

from src.agents import (
    triage_ticket,
    draft_response,
    judge_response,
    create_escalation_note,
    revise_response,
)
from src.gemini_agents import gemini_triage_ticket, gemini_draft_response, gemini_judge_response, gemini_create_escalation_note
from src.tools import policy_lookup
from src.schemas import FinalResult


console = Console()


def process_ticket(ticket_id: str, customer_message: str, mode: str = "rule") -> FinalResult:
    """Run the full Aegis support-agent pipeline for one ticket."""
    if mode == "gemini":
        triage_func = gemini_triage_ticket
        draft_func = gemini_draft_response
        judge_func = gemini_judge_response
        escalate_func = gemini_create_escalation_note
    else:
        triage_func = triage_ticket
        draft_func = draft_response
        judge_func = judge_response
        escalate_func = create_escalation_note
    triage = triage_func(customer_message)
    policy = policy_lookup(triage.category)
    draft = draft_func(customer_message, triage, policy)
    judge = judge_func(customer_message, triage, draft, policy)
        # Reflection Loop

    if judge.trust_score < 70:

        draft = revise_response(
            customer_message,
            triage,
            draft,
            judge,
            policy,
        )

        judge = judge_func(
            customer_message,
            triage,
            draft,
            policy,
        )

    escalation_note = None
    if judge.decision != "suggest_reply":
        escalation = escalate_func(customer_message, triage, judge)
        escalation_note = escalation.escalation_note

    return FinalResult(
        ticket_id=ticket_id,
        customer_message=customer_message,
        summary=triage.summary,
        category=triage.category,
        risk_level=judge.risk_level,
        policy=policy,
        draft_response=draft.response,
        trust_score=judge.trust_score,
        decision=judge.decision,
        reason=judge.reason,
        escalation_note=escalation_note,
    )


def print_result(result: FinalResult) -> None:
    """Pretty-print one final result."""
    console.print(Panel.fit(f"[bold]Ticket:[/bold] {result.ticket_id}", title="Aegis Support Agent"))
    console.print(f"[bold]Customer message:[/bold] {result.customer_message}")
    console.print(f"[bold]Summary:[/bold] {result.summary}")
    console.print(f"[bold]Category:[/bold] {result.category}")
    console.print(f"[bold]Risk level:[/bold] {result.risk_level}")
    console.print(f"[bold]Trust score:[/bold] {result.trust_score}")
    console.print(f"[bold]Decision:[/bold] {result.decision}")
    console.print(f"[bold]Reason:[/bold] {result.reason}")
    console.print()
    console.print(Panel(result.draft_response, title="Draft Response"))

    if result.escalation_note:
        console.print(Panel(result.escalation_note, title="Escalation / Human Review Note"))


def run_single_ticket(message: str, mode: str) -> None:
    result = process_ticket("manual", message, mode=mode)
    print_result(result)
    console.print()
    console.print("[bold]JSON output:[/bold]")
    console.print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))


def run_sample_file(path: str, mode: str) -> None:
    df = pd.read_csv(path)
    results = []

    for _, row in df.iterrows():
        result = process_ticket(row["ticket_id"], row["customer_message"], mode=mode)
        results.append(result.model_dump())
        print_result(result)
        console.print("-" * 80)

    output_path = "data/aegis_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    console.print(f"[green]Saved results to {output_path}[/green]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Aegis Support Agent")
    parser.add_argument("--message", type=str, help="Customer support ticket message")
    parser.add_argument("--sample", type=str, default=None, help="Path to sample tickets CSV")
    parser.add_argument("--mode", type=str, default="rule", choices=["rule", "gemini"], help="Agent mode: rule or gemini")
    args = parser.parse_args()
    console.print(f"[bold]Agent mode:[/bold] {args.mode}")

    if args.message:
        run_single_ticket(args.message, mode=args.mode)
    elif args.sample:
        run_sample_file(args.sample, mode=args.mode)
    else:
        console.print("[red]Please provide --message or --sample[/red]")
        console.print("Example:")
        console.print("python -m src.main --message 'I was charged twice this month. Please refund me now.'")
        console.print("python -m src.main --sample data/sample_tickets.csv")


if __name__ == "__main__":
    main()
