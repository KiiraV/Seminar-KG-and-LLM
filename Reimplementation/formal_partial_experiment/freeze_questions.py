#!/usr/bin/env python3
"""Freeze a benchmark slice and emit an answer-free graph seed manifest."""

import argparse
import json
from pathlib import Path


def answer_labels(item):
    labels = []
    for parse in item.get("Parses", []):
        for answer in parse.get("Answers", []):
            label = answer.get("EntityName") or answer.get("AnswerArgument")
            if label and label not in labels:
                labels.append(label)
    return labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="data/webqsp/webqsp_1000.json")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument(
        "--questions-out",
        default="formal_partial_experiment/data/frozen_questions.json",
    )
    parser.add_argument(
        "--seeds-out",
        default="formal_partial_experiment/data/graph_seeds.json",
    )
    args = parser.parse_args()

    source = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
    selected = source[: args.limit]
    frozen = []
    seeds = []
    for item in selected:
        record = dict(item)
        record["answer"] = answer_labels(item)
        record["mid_crucial_triples"] = []
        record.pop("crucial_triples", None)
        frozen.append(record)
        seeds.append(
            {
                "QuestionId": item["QuestionId"],
                "benchmark_index": item["index"],
                "topic_mids": sorted(item.get("topic_entity", {}).keys()),
                "topic_names": item.get("topic_entity", {}),
            }
        )

    questions_out = Path(args.questions_out)
    seeds_out = Path(args.seeds_out)
    questions_out.parent.mkdir(parents=True, exist_ok=True)
    questions_out.write_text(
        json.dumps(frozen, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    seeds_out.write_text(
        json.dumps(seeds, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"froze {len(frozen)} questions -> {questions_out}")
    print(f"wrote answer-free graph seeds -> {seeds_out}")


if __name__ == "__main__":
    main()
