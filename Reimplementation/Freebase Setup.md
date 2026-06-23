# Freebase Setup

## Decision

The Freebase API is closed, but Google still documents the historical RDF
dump. The complete triples archive is approximately 1.9 billion triples,
22 GB compressed, and 250 GB uncompressed. A full Virtuoso deployment is
outside the available laptop resources.

Following the tutor's recommendation, this reimplementation deploys Freebase
locally through Virtuoso but uses a partial dump. The benchmark is filtered so
that evaluation includes only questions answerable by that partial graph.

## Requirements

- Docker Desktop
- Python 3.9 virtual environment
- OpenLink Virtuoso Docker image
- Access to the independent QLever Freebase SPARQL endpoint
- The official GoG checkout

## Local Paths

```text
GoG repository:
/Users/kiira/Documents/Codex/2026-06-17/readme-md-https-github-com-yaooxu/GoG

Partial graph:
GoG/Freebase/virtuoso-opensource/database/FilterFreebase

Filtered benchmark:
GoG/data/webqsp_partial/data_with_ct_0.2_partial_answerable.json
```

## Partial-KG Construction Policy

1. Freeze the target question IDs.
2. Export only topic MIDs to the graph-construction manifest.
3. Retain a documented neighborhood from the independent QLever endpoint.
4. Include entity names, aliases, types, and necessary CVT nodes.
5. Avoid using `mid_crucial_triples` to construct the formal graph.
6. Import the graph into Virtuoso.
7. Execute gold SPARQL after construction and retain queries returning a gold answer.
8. Report selected count, retained count, and retention rate.

The helper `build_demo_partial_from_dataset.py` is an exception to step 5. It
exists only to validate the local pipeline and must not be used for scoring.

## Formal Pilot Service Layout

| Component | Location |
|---|---|
| QLever source | `https://qlever.dev/api/freebase` |
| Formal Virtuoso | `http://127.0.0.1:18892/sparql` |
| Formal BM25 | `http://127.0.0.1:18893/name2ids` |
| Local LLM | `http://127.0.0.1:11434/v1` |
| Model | `qwen2.5:7b` |

The documented Google dump link returned HTTP 403 during the experiment.
QLever enabled targeted independent extraction without using gold benchmark
triples.

## Start Virtuoso

From the GoG repository:

```bash
docker compose -f docker-compose.virtuoso.yml up -d
```

The SPARQL endpoint is:

```text
http://127.0.0.1:18890/sparql
```

## Import `FilterFreebase`

```bash
docker exec gog-virtuoso isql 1111 dba dba \
  exec="ld_dir('/opt/virtuoso-opensource/database', 'FilterFreebase', 'http://freebase.com'); rdf_loader_run(); checkpoint;"
```

## Verify SPARQL

```bash
.venv/bin/python scripts_partial/test_sparql.py \
  --mid m.078w2 \
  --sparql http://127.0.0.1:18890/sparql
```

The verified demo query returned `Samuel Taylor Coleridge`.

## Build and Test Entity Linking

```bash
.venv/bin/python scripts_partial/build_bm25_partial.py \
  --filter-freebase Freebase/virtuoso-opensource/database/FilterFreebase \
  --out Freebase/bm25.pkl

.venv/bin/python src/bm25_name2ids.py
```

In another terminal:

```bash
curl -X POST http://127.0.0.1:18891/name2ids \
  -H 'Content-Type: application/json' \
  -d '{"names":["Samuel Taylor Coleridge"]}'
```

The verified response contained MID `m.078w2` and type `people.person`.

## Full Command Sequence

The authoritative runnable guide is in the adjacent GoG checkout:

```text
GoG/RUN_PARTIAL.md
GoG/formal_partial_experiment/README.md
```

## Sources

- Google Freebase data dumps: https://developers.google.com/freebase
- Official GoG repository: https://github.com/YaooXu/GoG
