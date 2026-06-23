#!/usr/bin/env python3
"""Apply an answer-independent one-hop degree cap to frozen questions."""

import argparse
import json
from pathlib import Path


NS = "http://rdf.freebase.com/ns/"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--one-hop", required=True)
    parser.add_argument("--cap", type=int, default=10000)
    parser.add_argument("--questions-out", required=True)
    parser.add_argument("--seeds-out", required=True)
    args = parser.parse_args()

    questions = json.loads(Path(args.questions).read_text(encoding="utf-8"))
    mids = {
        mid
        for question in questions
        for mid in question.get("topic_entity", {})
    }
    degree = {mid: 0 for mid in mids}
    needles = {mid: f"<{NS}{mid}>" for mid in mids}
    for line in Path(args.one_hop).read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        subject, _, obj = parts[:3]
        for mid, needle in needles.items():
            if subject == needle or obj == needle:
                degree[mid] += 1

    eligible = []
    excluded = []
    for question in questions:
        topic_mids = sorted(question.get("topic_entity", {}))
        max_degree = max((degree[mid] for mid in topic_mids), default=0)
        record = {
            "QuestionId": question["QuestionId"],
            "topic_mids": topic_mids,
            "max_topic_degree": max_degree,
        }
        if max_degree <= args.cap:
            eligible.append(question)
        else:
            excluded.append(record)

    seeds = [
        {
            "QuestionId": item["QuestionId"],
            "benchmark_index": item["index"],
            "topic_mids": sorted(item.get("topic_entity", {})),
            "topic_names": item.get("topic_entity", {}),
        }
        for item in eligible
    ]
    Path(args.questions_out).write_text(
        json.dumps(eligible, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    Path(args.seeds_out).write_text(
        json.dumps(seeds, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    evidence = {
        "criterion": "maximum one-hop topic degree",
        "cap": args.cap,
        "eligible_count": len(eligible),
        "excluded": excluded,
        "all_topic_degrees": degree,
    }
    evidence_path = Path(args.questions_out).with_suffix(".degree_evidence.json")
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"degree cap kept {len(eligible)} / {len(questions)} questions")
    print(f"evidence -> {evidence_path}")


if __name__ == "__main__":
    main()
