## Full Freebase Deployment Limitation

The main reimplementation bottleneck is the Freebase setup. The original implementation requires a local Virtuoso deployment over the full Freebase dump. According to Google Freebase Data Dumps, the full Freebase triples contain approximately 1.9 billion triples, about 22 GB compressed and 250 GB uncompressed.

Due to storage and computation limitations, I cannot deploy the complete Freebase dump locally. Therefore, I follow the partial-dump strategy suggested by the tutor: deploy a partial Freebase dump through Virtuoso and filter the benchmark to retain only questions answerable by this partial KG.

This changes the evaluation setting. The results should be interpreted as partial-KG reimplementation results, not as a direct reproduction of the original full-Freebase results.

## Model Availability Limitation

The paper uses dated model versions such as `gpt-3.5-turbo-0613` and
`gpt-4-0613`. These versions are no longer generally available. A run with a
current model tests the implementation and method, but it is not an exact
model-level reproduction.

## Demo Data Leakage

The current 20-question demo graph is generated from benchmark-provided
`mid_crucial_triples`. This is useful for validating SPARQL, filtering, and
entity linking, but it exposes gold information. No accuracy score from this
graph is scientifically valid.

## Partial-KG Selection Bias

Filtering to answerable questions changes the benchmark population. Final
results must include the original selected count, retained count, retention
rate, graph-construction policy, and a coverage-adjusted score.
