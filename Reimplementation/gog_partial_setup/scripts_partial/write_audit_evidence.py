#!/usr/bin/env python3
"""Write machine-readable evidence for the current demo checkpoint."""

import argparse
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


def count_lines(path):
    with Path(path).open(encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default="data/webqsp_partial/data_with_ct_0.2_partial_answerable.json",
    )
    parser.add_argument("--out", default="results/demo_pipeline_evidence.json")
    args = parser.parse_args()

    paths = {
        "seed_mids": Path("data/webqsp_partial/seed_mids.txt"),
        "filter_freebase": Path(
            "Freebase/virtuoso-opensource/database/FilterFreebase"
        ),
        "bm25": Path("Freebase/bm25.pkl"),
        "strict_dataset": Path(args.dataset),
    }
    for path in paths.values():
        if not path.is_file():
            raise FileNotFoundError(path)

    samples = json.loads(paths["strict_dataset"].read_text(encoding="utf-8"))
    evidence = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "demo infrastructure validation only",
        "scientific_warning": "Gold crucial triples are present; no model score is valid.",
        "counts": {
            "seed_mids": count_lines(paths["seed_mids"]),
            "demo_triples": count_lines(paths["filter_freebase"]),
            "strict_gold_sparql_questions": len(samples),
            "bm25_bytes": paths["bm25"].stat().st_size,
        },
        "strict_question_ids": [sample.get("QuestionId") for sample in samples],
        "sha256": {name: sha256(path) for name, path in paths.items()},
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"wrote audit evidence to {out}")


if __name__ == "__main__":
    main()
