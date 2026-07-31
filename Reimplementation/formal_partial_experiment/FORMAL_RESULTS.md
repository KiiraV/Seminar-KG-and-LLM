# Formal Partial-Freebase Pilot Results

## Status

The experimental reproduction line has been completed as a small-scale pilot.
Unlike the engineering demo, this graph was not constructed from
benchmark-provided crucial triples.

## Protocol

- Source benchmark: first 10 WebQSP examples in benchmark order
- Graph source: public QLever Freebase endpoint
- Construction inputs: question ID, benchmark index, topic MID, topic name
- Forbidden construction inputs: answers, gold SPARQL, crucial triples
- Graph radius: incoming and outgoing one-hop Freebase triples
- Resource rule: exclude topic entities with one-hop degree above 10,000
- LLM: `qwen2.5:7b`, served locally by Ollama in Docker
- Temperature: `0`

Gold SPARQL was used only after graph construction to determine whether a
frozen question was executable on the partial graph.

## Population

| Stage | Questions |
|---|---:|
| Frozen before construction | 10 |
| Resource eligible | 9 |
| Gold-SPARQL answerable | 6 |
| Model evaluated | 6 |

`WebQTest-1637` was excluded by the answer-independent degree rule because the
Catholicism topic entity had 21,205 one-hop triples.

## Artifacts

| Artifact | Value |
|---|---:|
| Model graph entities | 4,536 |
| Model graph triples | 47,523 |
| BM25 names | 12,640 |
| SPARQL endpoint | local Virtuoso on port 18892 |
| BM25 endpoint | local Flask service on port 18893 |

## Result

The upstream evaluator reported 2 correct answers out of 6:

```text
2 / 6 = 33.3%
```

The upstream code labels the metric `Exact Match`, but its implementation
accepts a prediction when either normalized string contains the other. The
result is therefore described here as **relaxed answer match**, not strict
exact match.

Correct questions:

- county containing St. Louis Park: `Hennepin County`
- Marc Chagall's art type: `Surrealism`

## Interpretation

This result establishes that the complete experimental chain can run:

```text
frozen benchmark
  -> independent partial Freebase
  -> local Virtuoso
  -> strict answerability filtering
  -> graph-specific BM25
  -> GoG reasoning
  -> predictions
  -> evaluation
```

It does not reproduce the paper's benchmark score. The pilot differs in graph
coverage, sample size, model family, model scale, and multilingual label
selection. The low score is an experimental observation, not a failure of the
engineering pipeline.
