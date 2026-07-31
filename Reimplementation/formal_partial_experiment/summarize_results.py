#!/usr/bin/env python3
"""Summarize a formal pilot run into auditable JSON and CSV evidence."""

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relaxed_match(prediction, answers):
    response = " ".join(prediction).strip().lower()
    return any(
        response == answer.strip().lower()
        or response in answer.strip().lower()
        or answer.strip().lower() in response
        for answer in answers
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--model-graph", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--bm25", required=True)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--csv-out", required=True)
    args = parser.parse_args()

    predictions = json.loads(
        Path(args.predictions).read_text(encoding="utf-8")
    )
    rows = []
    for item in predictions:
        correct = relaxed_match(item["prediction"], item["ground_truth"])
        rows.append(
            {
                "index": item["index"],
                "question": item["question"],
                "prediction": " | ".join(item["prediction"]),
                "ground_truth": " | ".join(item["ground_truth"]),
                "relaxed_match": int(correct),
            }
        )

    csv_out = Path(args.csv_out)
    csv_out.parent.mkdir(parents=True, exist_ok=True)
    with csv_out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    right = sum(row["relaxed_match"] for row in rows)
    evidence = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "small-scale formal partial-Freebase pilot",
        "data_source": "https://qlever.dev/api/freebase",
        "selection": {
            "frozen_questions": 10,
            "resource_eligible_questions": 9,
            "degree_cap": 10000,
            "excluded_for_degree": ["WebQTest-1637"],
            "gold_sparql_answerable_questions": 6,
        },
        "graph": {
            "model_entities": 4536,
            "model_triples": 47523,
            "bm25_names": 12640,
        },
        "model": {
            "name": "qwen2.5:7b",
            "runtime": "Ollama in Docker",
            "ollama_model_id": "845dbda0ea48",
            "temperature": 0.0,
        },
        "result": {
            "correct": right,
            "evaluated": len(rows),
            "relaxed_answer_match": right / len(rows) if rows else 0.0,
        },
        "metric_note": (
            "The upstream evaluator calls this Exact Match, but it counts a "
            "question as correct when any normalized prediction/answer string "
            "contains the other. It is reported here as relaxed answer match."
        ),
        "sha256": {
            "model_graph": sha256(args.model_graph),
            "dataset": sha256(args.dataset),
            "bm25": sha256(args.bm25),
            "predictions": sha256(args.predictions),
        },
    }
    Path(args.json_out).write_text(
        json.dumps(evidence, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"formal pilot: {right}/{len(rows)} = "
        f"{evidence['result']['relaxed_answer_match']:.3f}"
    )


if __name__ == "__main__":
    main()
