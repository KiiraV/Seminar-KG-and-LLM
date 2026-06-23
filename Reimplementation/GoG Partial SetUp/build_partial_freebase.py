#!/usr/bin/env python3
"""Stream a one-hop Freebase subset around seed MIDs."""

import argparse
import gzip
import re
from pathlib import Path


MID_RE = re.compile(r"<http://rdf\.freebase\.com/ns/([mg]\.[A-Za-z0-9_]+)>")
METADATA = (
    "<http://rdf.freebase.com/ns/type.object.name>",
    "<http://rdf.freebase.com/ns/common.topic.alias>",
    "<http://rdf.freebase.com/ns/type.object.type>",
)


def open_text(path):
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="ignore")
    return open(path, "rt", encoding="utf-8", errors="ignore")


def mids_in_line(line):
    return set(MID_RE.findall(line))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freebase", required=True)
    parser.add_argument("--seeds", default="data/webqsp_partial/seed_mids.txt")
    parser.add_argument(
        "--out",
        default="Freebase/virtuoso-opensource/database/FilterFreebase",
    )
    parser.add_argument("--max-lines", type=int, default=0)
    args = parser.parse_args()

    seeds = {
        line.strip()
        for line in Path(args.seeds).read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    frontier = set(seeds)
    kept = 0
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("wt", encoding="utf-8") as output:
        print(f"pass 1: triples touching {len(seeds)} seed mids")
        with open_text(args.freebase) as handle:
            for i, line in enumerate(handle, start=1):
                mids = mids_in_line(line)
                if mids & seeds:
                    output.write(line)
                    frontier.update(mids)
                    kept += 1
                if args.max_lines and i >= args.max_lines:
                    break
                if i % 5_000_000 == 0:
                    print(f"scanned {i:,}; kept {kept:,}; frontier {len(frontier):,}")

        print(f"pass 2: metadata for {len(frontier)} one-hop mids")
        with open_text(args.freebase) as handle:
            for i, line in enumerate(handle, start=1):
                mids = mids_in_line(line)
                keep = (
                    any(predicate in line for predicate in METADATA)
                    and bool(mids & frontier)
                    and not bool(mids & seeds)
                )
                if keep:
                    output.write(line)
                    kept += 1
                if args.max_lines and i >= args.max_lines:
                    break
                if i % 5_000_000 == 0:
                    print(f"scanned {i:,}; kept {kept:,}")

    print(f"wrote {kept:,} triples to {out}")


if __name__ == "__main__":
    main()
