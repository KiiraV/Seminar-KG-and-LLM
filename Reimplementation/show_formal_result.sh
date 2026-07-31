#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 - <<'PY'
import csv
import json
from pathlib import Path

evidence_path = Path('formal_partial_experiment/results/experiment_evidence.json')
results_path = Path('formal_partial_experiment/results/per_question_results.csv')

evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
print('=== Formal Partial-Freebase Pilot Evidence ===')
print('Scope:', evidence['scope'])
print('Data source:', evidence['data_source'])
print()
print('Selection:')
for key, value in evidence['selection'].items():
    print(f'  {key}: {value}')
print()
print('Graph:')
for key, value in evidence['graph'].items():
    print(f'  {key}: {value}')
print()
print('Model:')
for key in ['name', 'runtime', 'temperature']:
    print(f'  {key}: {evidence["model"][key]}')
print()
print('Result:')
result = evidence['result']
print(f'  correct: {result["correct"]}')
print(f'  evaluated: {result["evaluated"]}')
print(f'  relaxed_answer_match: {result["relaxed_answer_match"]:.3f}')
print()
print('Per-question outcomes:')
with results_path.open(newline='', encoding='utf-8') as handle:
    reader = csv.DictReader(handle)
    for row in reader:
        mark = 'correct' if row['relaxed_match'] == '1' else 'wrong'
        print(f"  [{mark}] {row['question']} -> {row['prediction']} | gold: {row['ground_truth']}")
PY
