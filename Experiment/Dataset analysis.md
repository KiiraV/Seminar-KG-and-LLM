# Dataset Analysis: WebQSP and CWQ under Incomplete KG

## Benchmark Overview

The GoG paper uses two Freebase-based KGQA benchmarks:

- **WebQSP:** primarily one-hop and two-hop questions with executable SPARQL
  annotations.
- **ComplexWebQuestions (CWQ):** compositional questions requiring multi-hop
  reasoning, constraints, and aggregation.

The paper samples 1,000 questions from each dataset for IKGQA evaluation. The
local first target is the provided 1,000-question WebQSP IKG-20% file.

## Paper's IKG Construction

The paper identifies triples on each gold relation path and drops them with
probabilities of 20%, 40%, 60%, or 80%. When a crucial triple is dropped, the
relations between the same entity pair are also removed. This prevents a
system from reaching the answer through an equivalent edge.

## Local Partial-Dump Setting

The local experiment introduces a second form of incompleteness: only a
resource-bounded region of Freebase is deployed. The formal procedure is:

1. Freeze a subset of WebQSP question IDs.
2. Extract topic and answer MIDs.
3. construct a one-hop partial graph from an independent Freebase RDF dump;
4. include names, types, aliases, and necessary CVT connections;
5. load the graph into Virtuoso;
6. retain questions whose required entities are represented;
7. run GoG on the retained benchmark.

## Current Dataset Checkpoint

| Metric | Value | Interpretation |
|---|---:|---|
| WebQSP IKG-20% source questions | 1,000 | Official processed file |
| Demo questions selected | 20 | First 20 examples |
| Extracted seed MIDs | 124 | Topic and answer entities |
| Demo graph triples | 217 | Pipeline test only |
| Entity-covered demo questions | 20 | Weaker diagnostic |
| Strict gold-SPARQL answerable questions | 6 | Demo execution check |
| BM25 entity names | 123 | Built from the demo graph |

The demo graph uses benchmark-provided `mid_crucial_triples`. All 20 questions
have entity coverage, but only 6 gold SPARQL queries return a recorded answer.
Neither figure is a formal retention result because the graph contains gold
information.

## Formal Result Table

| Dataset | Selected | Retained | Retention rate | Partial-KG policy |
|---|---:|---:|---:|---|
| WebQSP pilot | 10 | 6 | 60.0% | independent one-hop Freebase neighborhood |

## Bias and Validity

Filtering by answerability changes the evaluation distribution. Accuracy on
the retained set may overestimate performance on the original sample.
Therefore, the final analysis will report both retained-set accuracy and
coverage-adjusted accuracy.

No Wikidata patches have been added in the current implementation. If they are
introduced later, their provenance and exact contribution must be documented.
