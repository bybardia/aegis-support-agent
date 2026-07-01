import argparse
import json
import pandas as pd
from rich.console import Console
from rich.table import Table

from src.main import process_ticket


console = Console()


def evaluate_sample(path: str, mode: str = "rule") -> dict:
    """Evaluate Aegis predictions against expected labels in a CSV file."""
    df = pd.read_csv(path)

    total = len(df)
    category_correct = 0
    risk_correct = 0
    decision_correct = 0
    rows = []

    for _, row in df.iterrows():
        result = process_ticket(row["ticket_id"], row["customer_message"], mode=mode)

        category_match = result.category == row["expected_category"]
        risk_match = result.risk_level == row["expected_risk"]
        decision_match = result.decision == row["expected_decision"]

        category_correct += int(category_match)
        risk_correct += int(risk_match)
        decision_correct += int(decision_match)

        rows.append({
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

    metrics = {
        "total": total,
        "category_accuracy": category_correct / total if total else 0,
        "risk_accuracy": risk_correct / total if total else 0,
        "decision_accuracy": decision_correct / total if total else 0,
    }

    return {"metrics": metrics, "rows": rows}


def save_evaluation(report: dict, output_path: str) -> None:
    """Save evaluation report as JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def print_evaluation(report: dict) -> None:
    metrics = report["metrics"]
    rows = report["rows"]

    console.print("[bold]Aegis Evaluation Report[/bold]")
    console.print(f"Total tickets: {metrics['total']}")
    console.print(f"Category accuracy: {metrics['category_accuracy']:.2%}")
    console.print(f"Risk accuracy: {metrics['risk_accuracy']:.2%}")
    console.print(f"Decision accuracy: {metrics['decision_accuracy']:.2%}")
    console.print()

    table = Table(title="Per-ticket Results")
    table.add_column("Ticket")
    table.add_column("Category")
    table.add_column("Risk")
    table.add_column("Decision")
    table.add_column("Trust")

    for row in rows:
        category = f"{row['predicted_category']} {'✅' if row['category_match'] else '❌'}"
        risk = f"{row['predicted_risk']} {'✅' if row['risk_match'] else '❌'}"
        decision = f"{row['predicted_decision']} {'✅' if row['decision_match'] else '❌'}"
        table.add_row(row["ticket_id"], category, risk, decision, str(row["trust_score"]))

    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Aegis Support Agent")
    parser.add_argument("--sample", type=str, default="data/sample_tickets.csv")
    parser.add_argument("--output", type=str, default="data/evaluation_report.json")
    parser.add_argument("--mode", type=str, default="rule", choices=["rule", "gemini"], help="Agent mode: rule or gemini")
    args = parser.parse_args()
    console.print(f"[bold]Agent mode:[/bold] {args.mode}")

    report = evaluate_sample(args.sample, mode=args.mode)
    print_evaluation(report)
    save_evaluation(report, args.output)
    console.print(f"[green]Saved evaluation report to {args.output}[/green]")


if __name__ == "__main__":
    main()
