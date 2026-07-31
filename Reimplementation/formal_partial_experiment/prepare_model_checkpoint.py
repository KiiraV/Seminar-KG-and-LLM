#!/usr/bin/env python3
"""Create a reduced one-hop checkpoint for the retained model population."""

import argparse
import json
from pathlib import Path


NS = "http://rdf.freebase.com/ns/"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--one-hop", required=True)
    parser.add_argument("--out-prefix", required=True)
    parser.add_argument("--seeds-out", required=True)
    args = parser.parse_args()

    questions = json.loads(Path(args.questions).read_text(encoding="utf-8"))
    seeds = {
        mid
        for question in questions
        for mid in question.get("topic_entity", {})
    }
    needles = {f"<{NS}{mid}>" for mid in seeds}
    triples = []
    frontier = set(seeds)
    for line in Path(args.one_hop).read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        s, _, o = parts[:3]
        if s not in needles and o not in needles:
            continue
        triples.append(line)
        for term in (s, o):
            if term.startswith(f"<{NS}") and term.endswith(">"):
                mid = term[len(NS) + 1 : -1]
                if mid.startswith(("m.", "g.")):
                    frontier.add(mid)

    prefix = Path(args.out_prefix)
    one_hop_out = prefix.with_suffix(".one_hop.nt")
    frontier_out = prefix.with_suffix(".frontier.json")
    one_hop_out.write_text("\n".join(sorted(set(triples))) + "\n")
    frontier_out.write_text(json.dumps(sorted(frontier), indent=2) + "\n")
    seed_manifest = [
        {
            "QuestionId": item["QuestionId"],
            "benchmark_index": item["index"],
            "topic_mids": sorted(item.get("topic_entity", {})),
            "topic_names": item.get("topic_entity", {}),
        }
        for item in questions
    ]
    Path(args.seeds_out).write_text(
        json.dumps(seed_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"prepared model checkpoint with {len(set(triples)):,} triples and "
        f"{len(frontier):,} entities"
    )


if __name__ == "__main__":
    main()
