# Reproduction Audit

## Purpose

This audit reran the local pipeline and separated three different claims:

1. **Deterministic preprocessing:** the same inputs generate identical files.
2. **Engineering operability:** local services and upstream interfaces work.
3. **Experimental completeness:** a valid model score can be reported.

## Repeat-Run Evidence

| Check | Repeat-run result |
|---|---|
| Seed extraction | 124 MIDs; SHA-256 identical |
| Demo KG generation | 217 triples; SHA-256 identical |
| Virtuoso RDF loader | Completed successfully |
| SPARQL name query | Returned Samuel Taylor Coleridge |
| GoG `get_1hop_triples` | Returned 6 triples and 2 relations |
| Entity-coverage diagnostic | 20/20 |
| Strict gold-SPARQL answerability | 6/20 |
| BM25 construction | 123 names; pickle SHA-256 identical |
| Name-to-ID endpoint | Returned `m.078w2` |
| `GoG.py --help` | Passed |
| `FreeBaseEnv` initialization | Passed; 300-dimensional spaCy vectors |
| Independent QLever graph | 47,523 triples; 4,536 model entities |
| Formal BM25 | 12,640 names |
| Local LLM run | Qwen2.5 7B through Ollama |
| Formal pilot evaluation | 2/6 relaxed answer match |

## Technical Erratum

The first version of `check_answerability.py` checked only whether topic and
answer MIDs occurred somewhere in the graph. This is entity coverage, not
strict answerability. The script now defaults to `--mode sparql`: it executes
the benchmark gold SPARQL and retains a question only when a returned value
matches a recorded gold answer.

Consequently, the demo checkpoint is:

- entity coverage: 20/20;
- strict executable answerability: 6/20.

The correction strengthens the methodology and does not invalidate the
Virtuoso, SPARQL, BM25, or preprocessing work.

## Known Non-Blocking Warnings

- macOS Python uses LibreSSL, producing an `urllib3` warning. Local HTTP and
  SPARQL requests still succeed.
- The demo builder assigns synthetic placeholder types to make the entity
  linking interface testable. Formal Freebase extraction will provide real
  types.
- The upstream environment variable is misspelled as `opeani_api_keys`.
- The installed OpenAI 0.27.9 package did not match the source's OpenAI 1.x
  client usage; the compatibility patch supports both interfaces.
- The upstream evaluator calls a substring-containment metric Exact Match and
  divided by zero in empty diagnostic categories.

## Remaining Paper-Level Blockers

1. The pilot contains only six evaluated questions.
2. Qwen2.5 7B differs from the paper's GPT configurations.
3. The graph is a one-hop partial graph rather than full Freebase.
4. The paper's exact 2023 model versions are no longer available.

## Verdict

Both reproduction tracks are complete at pilot scale. The engineering pipeline
is operational and deterministic. The independent experimental track produced
a recorded 2/6 result without crucial-triple leakage. This supports a
small-scale reimplementation claim, not a paper-level replication claim.
