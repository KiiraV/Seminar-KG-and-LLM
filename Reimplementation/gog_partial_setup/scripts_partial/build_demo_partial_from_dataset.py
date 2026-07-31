#!/usr/bin/env python3
"""Build a gold-leaking demo KG for infrastructure tests only."""

import argparse
import json
from pathlib import Path


NS = "http://rdf.freebase.com/ns/"


def uri(value):
    return f"<{NS}{value}>"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="data/webqsp/data_with_ct_0.2.json")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--out",
        default="Freebase/virtuoso-opensource/database/FilterFreebase",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
    data = data[: args.limit] if args.limit else data
    lines = set()

    for item in data:
        names = dict(item.get("topic_entity", {}))
        for parse in item.get("Parses", []):
            for answer in parse.get("Answers", []):
                mid = answer.get("AnswerArgument")
                name = answer.get("EntityName")
                if mid and name and mid.startswith(("m.", "g.")):
                    names[mid] = name
        for mid, name in names.items():
            literal = json.dumps(name, ensure_ascii=False) + "@en"
            lines.add(f"{uri(mid)}\t{uri('type.object.name')}\t{literal}\t.\n")
        for subject, predicate, obj in item.get("mid_crucial_triples", []):
            if subject.startswith(("m.", "g.")) and obj.startswith(("m.", "g.")):
                lines.add(f"{uri(subject)}\t{uri(predicate)}\t{uri(obj)}\t.\n")
                for mid in (subject, obj):
                    lines.add(
                        f"{uri(mid)}\t{uri('type.object.type')}\t"
                        f"{uri('people.person')}\t.\n"
                    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(sorted(lines)), encoding="utf-8")
    print(f"wrote {len(lines)} demo triples to {out}")
    print("warning: demo only; do not use for model evaluation")


if __name__ == "__main__":
    main()
