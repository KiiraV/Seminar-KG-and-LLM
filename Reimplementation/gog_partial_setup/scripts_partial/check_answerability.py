#!/usr/bin/env python3
"""Keep questions whose gold SPARQL returns a gold answer in local Virtuoso."""

import argparse
import json
import os
from pathlib import Path

from SPARQLWrapper import JSON, SPARQLWrapper


NS = "http://rdf.freebase.com/ns/"


def item_answers(item):
    values = set()
    for parse in item.get("Parses", []):
        for answer in parse.get("Answers", []):
            value = answer.get("AnswerArgument")
            if value:
                values.add(str(value))
    return values


def exists(sparql, mid):
    sparql.setQuery(
        f"""
PREFIX ns: <http://rdf.freebase.com/ns/>
ASK {{
  {{ ns:{mid} ?p ?o . }}
  UNION
  {{ ?s ?p ns:{mid} . }}
}}
"""
    )
    sparql.setReturnFormat(JSON)
    return bool(sparql.query().convert().get("boolean"))


def normalize(binding):
    value = str(binding.get("value", ""))
    return value[len(NS) :] if value.startswith(NS) else value


def executable_with_gold_answer(sparql, item):
    expected = item_answers(item)
    for parse in item.get("Parses", []):
        query = parse.get("Sparql")
        if not query:
            continue
        try:
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            bindings = sparql.query().convert().get("results", {}).get("bindings", [])
            returned = {normalize(row["x"]) for row in bindings if "x" in row}
            if returned & expected:
                return True
        except Exception as error:
            print(f"warning: SPARQL failed for {item.get('QuestionId')}: {error}")
    return False


def has_entity_coverage(sparql, item):
    topics = set(item.get("topic_entity", {}))
    answers = {
        value for value in item_answers(item) if value.startswith(("m.", "g."))
    }
    return (
        all(exists(sparql, mid) for mid in topics)
        and bool(answers)
        and any(exists(sparql, mid) for mid in answers)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="data/webqsp/data_with_ct_0.2.json")
    parser.add_argument(
        "--out",
        default="data/webqsp_partial/data_with_ct_0.2_partial_answerable.json",
    )
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--sparql",
        default=os.environ.get("SPARQLPATH", "http://127.0.0.1:18890/sparql"),
    )
    parser.add_argument(
        "--mode",
        choices=("sparql", "entity-coverage"),
        default="sparql",
        help="sparql is strict; entity-coverage is a weaker diagnostic",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
    data = data[: args.limit] if args.limit else data
    sparql = SPARQLWrapper(args.sparql)
    kept = []

    for item in data:
        if args.mode == "sparql":
            answerable = executable_with_gold_answer(sparql, item)
        else:
            answerable = has_entity_coverage(sparql, item)
        if answerable:
            kept.append(item)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(kept, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"mode={args.mode}; kept {len(kept)} / {len(data)} questions -> {out}")


if __name__ == "__main__":
    main()
