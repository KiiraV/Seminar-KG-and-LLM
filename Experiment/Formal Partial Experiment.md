# Formal Partial-Freebase Experiment

## Experimental question

Can the GoG pipeline produce evaluated predictions on a small independently
constructed partial Freebase graph?

## Design

The first ten WebQSP examples were frozen before graph construction. A separate
seed manifest exposed only question IDs and topic MIDs. Incoming and outgoing
one-hop triples were retrieved from the public QLever Freebase endpoint.
Answers, gold SPARQL, and benchmark crucial triples were not read during graph
construction.

A one-hop topic-degree cap of 10,000 was applied as an answer-independent
resource rule. Nine questions remained eligible. Gold SPARQL was then executed
against the local graph, retaining six answerable questions.

The model graph contained 4,536 entities and 47,523 triples. Its BM25 index
contained 12,640 names. GoG was run with the locally served `qwen2.5:7b` model
at temperature zero.

## Result

| Measure | Result |
|---|---:|
| Frozen questions | 10 |
| Resource eligible | 9 |
| Gold-SPARQL answerable | 6 |
| Correct predictions | 2 |
| Relaxed answer match | 33.3% |

The upstream evaluator calls this metric `Exact Match`, but its implementation
uses normalized substring overlap. It is therefore reported as relaxed answer
match.

## Interpretation

The result completes a small-scale experimental reproduction, but it is not
directly comparable with the paper. The graph is much smaller, the evaluation
population contains six questions, and Qwen2.5 7B replaces the unavailable
paper model. The experiment is evidence that the full scientific workflow can
be executed without gold-triple leakage.

The multilingual labels observed in retrieved Freebase metadata are a source
of model error and should be discussed as a limitation of the pilot.
