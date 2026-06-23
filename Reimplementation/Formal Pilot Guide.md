# Formal Partial-Freebase Pilot Guide

This guide records the independent experimental track. It is designed to avoid
using benchmark answers or crucial triples during graph construction.
The reusable orchestration files and scripts are published in
[`gog_formal_setup/`](gog_formal_setup/).

## Procedure

1. Freeze the WebQSP question IDs before graph construction.
2. Export only topic MIDs.
3. Retrieve incoming and outgoing one-hop triples from
   [QLever Freebase](https://qlever.dev/freebase).
4. Apply an answer-independent degree cap.
5. Import the resulting graph into a separate Virtuoso instance.
6. Execute gold SPARQL only after graph construction.
7. Retain questions for which the partial graph returns a gold answer.
8. Enrich the retained graph with names, aliases, types, and required CVT
   nodes.
9. Build BM25 from that exact graph.
10. Run GoG and archive predictions, per-question results, configuration, and
    hashes.

Apply the package to a clean GoG checkout:

```bash
cp -R /path/to/Seminar-KG-and-LLM/Reimplementation/gog_formal_setup/. \
  /path/to/GoG/
cd /path/to/GoG
git apply upstream_compatibility.patch
```

The formal package shares the BM25 and preflight utilities from
[`gog_partial_setup/`](gog_partial_setup/). Copy that package into the same GoG
checkout before running the formal targets.

## Verified configuration

| Component | Value |
|---|---|
| Dataset | WebQSP |
| Frozen questions | 10 |
| Degree cap | 10,000 triples per topic |
| Resource-eligible questions | 9 |
| Answerable questions | 6 |
| Model graph | 47,523 triples / 4,536 entities |
| BM25 names | 12,640 |
| LLM | Qwen2.5 7B via Ollama |
| Temperature | 0 |

Services were isolated from the demo track:

```text
Formal Virtuoso: http://127.0.0.1:18892/sparql
Formal BM25:     http://127.0.0.1:18893/name2ids
Local LLM:       http://127.0.0.1:11434/v1
```

These are local service addresses, not downloadable web resources.

## Result and interpretation

The retained-set relaxed answer match was 2/6. Relative to the original frozen
set, the coverage-adjusted result was 2/10.

Report both values. The retained-set result measures model performance after
graph filtering, while the coverage-adjusted result also reflects questions
that the partial graph could not support.

## Files intentionally not published

The repository does not include:

- Virtuoso database files;
- generated RDF graphs;
- model weights or Ollama volumes;
- raw model logs and large intermediate checkpoints;
- `.env` files or credentials.

The published package contains source scripts and configuration, while the
evidence JSON records the final counts and model configuration. See
[Formal Partial Experiment](../Experiment/Formal%20Partial%20Experiment.md),
the [formal setup package](gog_formal_setup/), and the
[reproduction audit](Reproduction%20Audit.md).

