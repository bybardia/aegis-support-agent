import argparse
import json
import pandas as pd
from rich.console import Console
from rich.table import Table

from src.main import process_ticket


console = Console()


def build_confusion_matrix(sample_path: str, mode: str = "rule") -> dict:
    df = pd.read_csv(sample_path)

    category_rows = []
    risk_rows = []
    decision_rows = []

    for _, row in df.iterrows():
        result = process_ticket(row["ticket_id"], row["customer_message"], mode=mode)

        category_rows.append({
            "expected": row["expected_category"],
            "predicted": result.category,
        })
        risk_rows.append({
            "expected": row["expected_risk"],
            "predicted": result.risk_level,
        })
        decision_rows.append({
            "expected": row["expected_decision"],
            "predicted": result.decision,
        })

    return {
        "mode": mode,
        "category": pd.crosstab(
            pd.Series([r["expected"] for r in category_rows], name="expected"),
            pd.Series([r["predicted"] for r in category_rows], name="predicted"),
        ).to_dict(),
        "risk": pd.crosstab(
            pd.Series([r["expected"] for r in risk_rows], name="expected"),
            pd.Series([r["predicted"] for r in risk_rows], name="predicted"),
        ).to_dict(),
        "decision": pd.crosstab(
            pd.Series([r["expected"] for r in decision_rows], name="expected"),
            pd.Series([r["predicted"] for r in decision_rows], name="predicted"),
        ).to_dict(),
    }


def print_matrix(title: str, matrix_dict: dict) -> None:
    console.print(f"[bold]{title}[/bold]")

    if not matrix_dict:
        console.print("[yellow]No data[/yellow]")
        return

    predicted_labels = sorted(matrix_dict.keys())
    expected_labels = sorted({
        label
        for predicted in matrix_dict.values()
        for label in predicted.keys()
    })

    table = Table(title=title)
    table.add_column("Expected \\ Predicted")

    for label in predicted_labels:
        table.add_column(label)

    for expected in expected_labels:
        row_values = [expected]
        for predicted in predicted_labels:
            row_values.append(str(matrix_dict.get(predicted, {}).get(expected, 0)))
        table.add_row(*row_values)

    console.print(table)
    console.print()


def save_report(report: dict, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aegis Confusion Matrix")
    parser.add_argument("--sample", type=str, default="data/sample_tickets.csv")
    parser.add_argument("--mode", type=str, default="rule", choices=["rule", "gemini"])
    parser.add_argument("--output", type=str, default="data/confusion_matrix.json")
    args = parser.parse_args()

    report = build_confusion_matrix(args.sample, mode=args.mode)

    console.print(f"[bold]Agent mode:[/bold] {args.mode}")
    print_matrix("Category Confusion Matrix", report["category"])
    print_matrix("Risk Confusion Matrix", report["risk"])
    print_matrix("Decision Confusion Matrix", report["decision"])

    save_report(report, args.output)
    console.print(f"[green]Saved confusion matrix to {args.output}[/green]")


if __name__ == "__main__":
    main()
