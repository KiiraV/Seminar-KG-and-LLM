#!/usr/bin/env python3
"""Extract topic and answer Freebase MIDs from a GoG/WebQSP dataset."""

import argparse
import json
import re
from pathlib import Path


MID_RE = re.compile(r"^[mg]\.[A-Za-z0-9_]+$")


def answer_mids(item):
    mids = set()
    for parse in item.get("Parses", []):
        for answer in parse.get("Answers", []):
            value = answer.get("AnswerArgument")
            if value and MID_RE.match(value):
                mids.add(value)
    return mids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="data/webqsp/data_with_ct_0.2.json")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--out", default="data/webqsp_partial/seed_mids.txt")
    args = parser.parse_args()

    data = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
    if args.limit:
        data = data[: args.limit]

    mids = set()
    for item in data:
        mids.update(item.get("topic_entity", {}).keys())
        mids.update(answer_mids(item))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(mids)) + "\n", encoding="utf-8")
    print(f"wrote {len(mids)} seed mids to {out}")


if __name__ == "__main__":
    main()
