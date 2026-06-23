# Experiment Protocol

## Objective

Evaluate whether GoG can run and answer questions against a locally deployed
partial Freebase graph.

## Phase A: Infrastructure Validation

This phase is complete.

| Item | Value |
|---|---:|
| Source benchmark | WebQSP IKG-20% |
| Source benchmark size | 1,000 |
| Demo questions selected | 20 |
| Seed MIDs | 124 |
| Demo KG triples | 217 |
| Entity-covered demo questions | 20 |
| Strict gold-SPARQL answerable questions | 6 |
| BM25 names | 123 |

The demo graph uses benchmark-provided crucial triples. The 20/20 figure is
entity coverage; strict query execution retains 6/20. It validates software
interfaces but is invalid for measuring GoG accuracy.

## Phase B: Formal Partial-KG Experiment

This phase has now been completed as a six-question pilot. See
[`Formal Partial Experiment.md`](Formal%20Partial%20Experiment.md).

1. Ten WebQSP question IDs were frozen before graph construction.
2. A one-hop graph was independently retrieved from QLever Freebase.
3. An answer-independent degree cap retained 9/10 questions.
4. Gold-SPARQL filtering retained 6/9 questions.
5. The enriched model graph contained 47,523 triples and 4,536 entities.
6. BM25 indexed 12,640 names from the same graph.
7. GoG ran with local Qwen2.5 7B at temperature zero.
8. The upstream relaxed answer-match implementation scored 2/6.

## Primary Metrics

- Retention rate: answerable questions / selected questions.
- Hits@1 or exact match on the retained subset.
- Coverage-adjusted accuracy: correct answers / originally selected questions.
- Average Search and Generate actions per question.
- Fallback-to-LLM-only rate.

## Reporting Rule

Never compare a partial-KG score directly with the paper's full-Freebase score
without also reporting graph construction, selected count, retained count, and
retention rate.
