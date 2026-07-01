#!/usr/bin/env bash
set -e

MODE="${1:-rule}"
SAMPLE_PATH="data/sample_tickets.csv"

echo "========================================"
echo "Aegis Support Agent - Full Run"
echo "Mode: $MODE"
echo "Sample: $SAMPLE_PATH"
echo "========================================"

echo
echo "1. Running support-agent pipeline..."
python -m src.main --sample "$SAMPLE_PATH" --mode "$MODE"

echo
echo "2. Running evaluation..."
python -m src.evaluator --sample "$SAMPLE_PATH" --mode "$MODE"

echo
echo "3. Running error analysis..."
python -m src.error_analysis --sample "$SAMPLE_PATH" --mode "$MODE"

echo
echo "4. Running confusion matrix..."
python -m src.confusion_matrix --sample "$SAMPLE_PATH" --mode "$MODE"

echo
echo "========================================"
echo "Done."
echo "Generated files:"
echo "- data/aegis_results.json"
echo "- data/evaluation_report.json"
echo "- data/error_analysis.json"
echo "- data/confusion_matrix.json"
echo "========================================"
