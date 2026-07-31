#!/usr/bin/env python3
"""Smoke-test the local Freebase SPARQL endpoint."""

import argparse
import os

from SPARQLWrapper import JSON, SPARQLWrapper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mid", default="m.078w2")
    parser.add_argument(
        "--sparql",
        default=os.environ.get("SPARQLPATH", "http://127.0.0.1:18890/sparql"),
    )
    args = parser.parse_args()

    sparql = SPARQLWrapper(args.sparql)
    sparql.setQuery(
        f"""
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?name WHERE {{
  ns:{args.mid} ns:type.object.name ?name .
}}
LIMIT 10
"""
    )
    sparql.setReturnFormat(JSON)
    print(sparql.query().convert())


if __name__ == "__main__":
    main()
