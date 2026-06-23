# Reimplementation Status

## Verified Checkpoint

| Stage | Status | Verified evidence |
|---|---|---|
| Clone and environment | Complete | GoG imports succeed |
| Python dependencies | Complete | spaCy model and vectors load |
| Virtuoso deployment | Complete | Docker service and SPARQL HTTP 200 |
| Seed extraction | Complete | 124 MIDs from 20 WebQSP questions |
| Demo graph | Complete | 217 triples |
| SPARQL retrieval | Complete | MID `m.078w2` resolves correctly |
| Entity-coverage diagnostic | Complete | 20/20 demo questions |
| Strict gold-SPARQL filtering | Complete | 6/20 demo questions |
| BM25 construction | Complete | 123 names |
| Name-to-ID service | Complete | typed MID response returned |
| Independent partial Freebase | Complete pilot | 47,523 triples from QLever Freebase |
| LLM execution | Complete pilot | Local Qwen2.5 7B via Ollama |
| Final pilot evaluation | Complete | 2/6 relaxed answer match |

## Scientific Validity Boundary

The current demo graph is generated from `mid_crucial_triples` contained in
the benchmark. It is intentionally used only to test the plumbing. It includes
gold information and cannot be used to claim a GoG accuracy result.

## Formal Result Template

| Dataset | Selected | Retained | Retention rate | KG policy | Model | Score |
|---|---:|---:|---:|---|---|---:|
| WebQSP pilot | 10 | 6 | 60.0% of frozen set | independent one-hop partial Freebase | Qwen2.5 7B | 33.3% relaxed match |

## Expected Output Locations

```text
GoG/data/webqsp_partial/data_with_ct_0.2_partial_answerable.json
GoG/results/<model>/webqsp_partial/*.jsonl
GoG/results/<model>/webqsp_partial/*.json
GoG/results/<model>/webqsp_partial/*.log
```
