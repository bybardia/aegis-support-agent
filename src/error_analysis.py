import argparse
import json
import pandas as pd
from rich.console import Console
from rich.table import Table

from src.main import process_ticket


console = Console()


def analyze_errors(sample_path: str, mode: str = "rule") -> dict:
    df = pd.read_csv(sample_path)
    errors = []

    for _, row in df.iterrows():
        result = process_ticket(row["ticket_id"], row["customer_message"], mode=mode)

        category_match = result.category == row["expected_category"]
        risk_match = result.risk_level == row["expected_risk"]
        decision_match = result.decision == row["expected_decision"]

        if not (category_match and risk_match and decision_match):
            errors.append({
                "ticket_id": row["ticket_id"],
                "customer_message": row["customer_message"],
                "expected_category": row["expected_category"],
                "predicted_category": result.category,
                "category_match": category_match,
                "expected_risk": row["expected_risk"],
                "predicted_risk": result.risk_level,
                "risk_match": risk_match,
                "expected_decision": row["expected_decision"],
                "predicted_decision": result.decision,
                "decision_match": decision_match,
                "trust_score": result.trust_score,
                "reason": result.reason,
            })

    return {
        "mode": mode,
        "total_tickets": len(df),
        "error_count": len(errors),
        "errors": errors,
    }


def print_errors(report: dict) -> None:
    console.print("[bold]Aegis Error Analysis[/bold]")
    console.print(f"Mode: {report['mode']}")
    console.print(f"Total tickets: {report['total_tickets']}")
    console.print(f"Errors: {report['error_count']}")
    console.print()

    if not report["errors"]:
        console.print("[green]No errors found.[/green]")
        return

    table = Table(title="Mismatched Tickets")
    table.add_column("Ticket")
    table.add_column("Message")
    table.add_column("Category")
    table.add_column("Risk")
    table.add_column("Decision")
    table.add_column("Trust")

    for err in report["errors"]:
        category = f"{err['expected_category']} → {err['predicted_category']}"
        risk = f"{err['expected_risk']} → {err['predicted_risk']}"
        decision = f"{err['expected_decision']} → {err['predicted_decision']}"
        message = err["customer_message"][:60]
        table.add_row(err["ticket_id"], message, category, risk, decision, str(err["trust_score"]))

    console.print(table)


def save_report(report: dict, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aegis Error Analysis")
    parser.add_argument("--sample", type=str, default="data/sample_tickets.csv")
    parser.add_argument("--mode", type=str, default="rule", choices=["rule", "gemini"])
    parser.add_argument("--output", type=str, default="data/error_analysis.json")
    args = parser.parse_args()

    report = analyze_errors(args.sample, mode=args.mode)
    print_errors(report)
    save_report(report, args.output)
    console.print(f"[green]Saved error analysis to {args.output}[/green]")


if __name__ == "__main__":
    main()
