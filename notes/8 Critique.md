# Strengths

- The task reflects realistic knowledge-graph incompleteness.
- Search and generation are integrated in one explicit agent loop.
- Reasoning traces are inspectable.
- The method is training-free and can use different LLM backbones.
- The paper evaluates several degrees of missing crucial triples.

# Limitations

## Self-verification bias

The same LLM family may generate and verify a triple. A confidently generated
false fact can therefore be accepted by a verifier with similar biases.

## Error propagation

An incorrect entity link, relation choice, or generated triple becomes context
for later reasoning steps.

## Cost and latency

A single question can require calls for planning, relation filtering,
generation, verification, and entity selection.

## Model dependence

Performance varies strongly by backbone. The exact models used in the paper
may become unavailable, reducing long-term reproducibility.

## Evaluation realism

Randomly dropping annotated crucial triples creates a controlled benchmark,
but real KG incompleteness may be systematic rather than random.

# Reimplementation-Specific Threats

- Filtering to questions answerable by a partial graph creates selection bias.
- A benchmark-centered graph may contain fewer distractors than full Freebase.
- A graph built from gold crucial triples leaks evaluation information and is
  suitable only for infrastructure testing.
- Partial-KG accuracy must be reported together with graph coverage and
  retained question count.

# Improvement Ideas

- Verify generated triples with an independent source or second model.
- Report calibrated confidence for generated knowledge.
- Compare one-hop and two-hop partial-graph construction.
- Report coverage-adjusted accuracy in addition to retained-set accuracy.
- Separate failures into retrieval, entity linking, generation, verification,
  and answer-formatting categories.

