#!/usr/bin/env python3
"""Extract a one-hop partial Freebase graph from QLever without gold data."""

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


NS = "http://rdf.freebase.com/ns/"
METADATA = (
    "type.object.name",
    "common.topic.alias",
    "type.object.type",
)


def query(endpoint, sparql, retries=8):
    body = urllib.parse.urlencode({"query": sparql}).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "GoG-seminar-reimplementation/1.0",
        },
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if attempt + 1 == retries:
                raise
            if error.code == 429:
                delay = int(error.headers.get("Retry-After", "30"))
            else:
                delay = min(60, 2 ** attempt)
            print(f"request failed with HTTP {error.code}; retrying in {delay}s")
            time.sleep(delay)
        except Exception as error:
            if attempt + 1 == retries:
                raise
            delay = min(60, 2 ** attempt)
            print(f"request failed: {error}; retrying in {delay}s")
            time.sleep(delay)


def escape_literal(value):
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


def term_nt(term):
    kind = term["type"]
    value = term["value"]
    if kind == "uri":
        return f"<{value}>"
    if kind == "bnode":
        return f"_:{value}"
    literal = f'"{escape_literal(value)}"'
    if term.get("xml:lang"):
        return f"{literal}@{term['xml:lang']}"
    if term.get("datatype"):
        return f"{literal}^^<{term['datatype']}>"
    return literal


def values(mids):
    return " ".join(f"<{NS}{mid}>" for mid in mids)


def paged_bindings(endpoint, query_body, page_size):
    offset = 0
    while True:
        result = query(
            endpoint,
            f"{query_body}\nLIMIT {page_size}\nOFFSET {offset}",
        )
        bindings = result.get("results", {}).get("bindings", [])
        yield from bindings
        if len(bindings) < page_size:
            break
        offset += page_size


def load_seed_mids(path):
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    return sorted(
        {
            mid
            for item in manifest
            for mid in item.get("topic_mids", [])
        }
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--endpoint",
        default="https://qlever.dev/api/freebase",
    )
    parser.add_argument(
        "--seeds",
        default="formal_partial_experiment/data/graph_seeds.json",
    )
    parser.add_argument(
        "--out",
        default="formal_partial_experiment/data/FormalFreebase.nt",
    )
    parser.add_argument("--page-size", type=int, default=10000)
    parser.add_argument("--metadata-chunk", type=int, default=100)
    parser.add_argument("--request-delay", type=float, default=1.0)
    parser.add_argument(
        "--skip-metadata",
        action="store_true",
        help="write the complete one-hop relation graph before metadata enrichment",
    )
    args = parser.parse_args()

    seeds = load_seed_mids(args.seeds)
    out = Path(args.out)
    one_hop_cache = out.with_suffix(".one_hop.nt")
    frontier_cache = out.with_suffix(".frontier.json")
    triples = set()
    frontier = set(seeds)
    if one_hop_cache.exists() and frontier_cache.exists():
        for line in one_hop_cache.read_text(encoding="utf-8").splitlines():
            s, p, o, _ = line.split("\t", 3)
            triples.add((s, p, o))
        frontier.update(
            json.loads(frontier_cache.read_text(encoding="utf-8"))
        )
        print(
            f"loaded one-hop checkpoint: {len(triples):,} triples, "
            f"{len(frontier):,} entities"
        )
    else:
        print(f"retrieving one-hop graph for {len(seeds)} frozen topic MIDs")
        for seed_index, seed in enumerate(seeds, start=1):
            for direction, pattern in (
                ("outgoing", f"BIND(<{NS}{seed}> AS ?s) ?s ?p ?o ."),
                ("incoming", f"?s ?p <{NS}{seed}> . BIND(<{NS}{seed}> AS ?o)"),
            ):
                one_hop_query = f"""
SELECT DISTINCT ?s ?p ?o WHERE {{
  {pattern}
  FILTER(STRSTARTS(STR(?p), "{NS}"))
}}
"""
                before = len(triples)
                for binding in paged_bindings(
                    args.endpoint,
                    one_hop_query,
                    args.page_size,
                ):
                    triple = tuple(term_nt(binding[key]) for key in ("s", "p", "o"))
                    triples.add(triple)
                    for key in ("s", "o"):
                        term = binding[key]
                        if term["type"] == "uri" and term["value"].startswith(NS):
                            mid = term["value"][len(NS) :]
                            if mid.startswith(("m.", "g.")):
                                frontier.add(mid)
                print(
                    f"  {seed_index}/{len(seeds)} {seed} {direction}: "
                    f"+{len(triples) - before:,} triples"
                )
                time.sleep(args.request_delay)
        out.parent.mkdir(parents=True, exist_ok=True)
        with one_hop_cache.open("w", encoding="utf-8") as handle:
            for s, p, o in sorted(triples):
                handle.write(f"{s}\t{p}\t{o}\t.\n")
        frontier_cache.write_text(
            json.dumps(sorted(frontier), indent=2) + "\n",
            encoding="utf-8",
        )
        print(
            f"saved one-hop checkpoint: {one_hop_cache} and {frontier_cache}"
        )

    predicates = " ".join(f"<{NS}{predicate}>" for predicate in METADATA)
    frontier_list = sorted(frontier)
    if not args.skip_metadata:
        print(f"retrieving metadata for {len(frontier_list)} graph entities")
        chunk_starts = list(range(0, len(frontier_list), args.metadata_chunk))
        for chunk_number, start in enumerate(chunk_starts, start=1):
            chunk = frontier_list[start : start + args.metadata_chunk]
            metadata_query = f"""
SELECT DISTINCT ?s ?p ?o WHERE {{
  VALUES ?s {{ {values(chunk)} }}
  VALUES ?p {{ {predicates} }}
  ?s ?p ?o .
}}
"""
            for binding in paged_bindings(
                args.endpoint,
                metadata_query,
                args.page_size,
            ):
                triples.add(tuple(term_nt(binding[key]) for key in ("s", "p", "o")))
            if chunk_number % 10 == 0 or chunk_number == len(chunk_starts):
                print(
                    f"  metadata {chunk_number}/{len(chunk_starts)} chunks; "
                    f"{len(triples):,} total triples"
                )
            time.sleep(args.request_delay)
    else:
        print("metadata enrichment deferred until after answerability filtering")

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for s, p, o in sorted(triples):
            handle.write(f"{s}\t{p}\t{o}\t.\n")

    evidence = {
        "source": args.endpoint,
        "construction_inputs": [
            "QuestionId",
            "benchmark_index",
            "topic_mids",
            "topic_names",
        ],
        "forbidden_inputs": [
            "Answers",
            "gold SPARQL",
            "mid_crucial_triples",
            "crucial_triples",
        ],
        "seed_mid_count": len(seeds),
        "frontier_mid_count": len(frontier),
        "triple_count": len(triples),
        "metadata_enriched": not args.skip_metadata,
    }
    evidence_path = out.with_suffix(".evidence.json")
    evidence_path.write_text(
        json.dumps(evidence, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(triples):,} triples -> {out}")
    print(f"wrote construction evidence -> {evidence_path}")


if __name__ == "__main__":
    main()
