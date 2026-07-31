#!/usr/bin/env python3
"""Build Freebase/bm25.pkl from a small partial FilterFreebase file."""

import argparse
import os
import pickle
import sys
from collections import defaultdict
from pathlib import Path

from rank_bm25 import BM25Okapi

sys.path.append("src")
from bm25_name2ids import BM25Retrieve  # noqa: E402


def parse_name_literal(raw):
    if raw.endswith("@en"):
        raw = raw[:-3]
    return raw.strip('"').lower()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filter-freebase",
        default="Freebase/virtuoso-opensource/database/FilterFreebase",
    )
    parser.add_argument("--out", default="Freebase/bm25.pkl")
    args = parser.parse_args()

    name_to_ids = defaultdict(set)
    with Path(args.filter_freebase).open(encoding="utf-8") as handle:
        for line in handle:
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            subject, predicate, obj = parts[:3]
            if predicate != "<http://rdf.freebase.com/ns/type.object.name>":
                continue
            mid = subject.rsplit("/", 1)[-1].strip(">")
            if mid.startswith(("m.", "g.")):
                name_to_ids[parse_name_literal(obj)].add(mid)

    retrieve = BM25Retrieve.__new__(BM25Retrieve)
    retrieve.name_to_ids = {
        name: sorted(ids) for name, ids in name_to_ids.items()
    }
    retrieve.all_fns = list(retrieve.name_to_ids)
    retrieve.tokenized_all_fns = [name.split() for name in retrieve.all_fns]
    retrieve.bm25_all_fns = BM25Okapi(retrieve.tokenized_all_fns)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as handle:
        pickle.dump(retrieve, handle)
    print(f"wrote BM25 index with {len(retrieve.name_to_ids)} names to {out}")


if __name__ == "__main__":
    os.environ.setdefault("SPARQLPATH", "http://127.0.0.1:18890/sparql")
    main()
