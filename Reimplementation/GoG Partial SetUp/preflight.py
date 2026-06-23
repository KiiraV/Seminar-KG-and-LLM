#!/usr/bin/env python3
"""Check partial-KG files and services before running GoG."""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
from SPARQLWrapper import JSON, SPARQLWrapper


def report(name, ok, detail):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default="data/webqsp_partial/data_with_ct_0.2_partial_answerable.json",
    )
    parser.add_argument("--skip-llm", action="store_true")
    args = parser.parse_args()
    load_dotenv()
    checks = []

    try:
        samples = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
        checks.append(report("dataset", bool(samples), f"{len(samples)} samples"))
    except Exception as error:
        checks.append(report("dataset", False, str(error)))

    for name, path in (
        ("partial KG file", Path("Freebase/virtuoso-opensource/database/FilterFreebase")),
        ("BM25 index", Path("Freebase/bm25.pkl")),
    ):
        checks.append(report(name, path.is_file() and path.stat().st_size > 0, str(path)))

    sparql_url = os.environ.get("SPARQLPATH", "http://127.0.0.1:18890/sparql")
    try:
        sparql = SPARQLWrapper(sparql_url)
        sparql.setQuery("ASK { ?s ?p ?o }")
        sparql.setReturnFormat(JSON)
        checks.append(report("SPARQL", bool(sparql.query().convert().get("boolean")), sparql_url))
    except Exception as error:
        checks.append(report("SPARQL", False, str(error)))

    try:
        response = requests.post(
            "http://127.0.0.1:18891/name2ids",
            json={"names": ["Samuel Taylor Coleridge"]},
            timeout=5,
        )
        payload = response.json()
        checks.append(
            report(
                "name-to-ID service",
                response.ok and payload.get("status") == "success",
                f"HTTP {response.status_code}",
            )
        )
    except Exception as error:
        checks.append(report("name-to-ID service", False, str(error)))

    if args.skip_llm:
        print("[SKIP] LLM configuration")
    else:
        key = os.environ.get("opeani_api_keys", "")
        base_url = os.environ.get("base_url", "")
        checks.append(report("LLM base URL", bool(base_url), base_url or "missing"))
        valid_key = bool(key) and "replace_with" not in key and key != "placeholder"
        checks.append(report("LLM API key", valid_key, "configured" if valid_key else "missing/placeholder"))

    if not all(checks):
        sys.exit(1)
    print("Preflight passed.")


if __name__ == "__main__":
    main()
