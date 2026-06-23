# Experiment

This note summarizes the role of the experiment section in the seminar
reimplementation. The detailed protocol, evidence files, and result tables are
kept in the [`Experiment`](../Experiment/) folder to avoid duplicating the same
material in two places.

## Purpose

The experiment is designed to show that the GoG pipeline can be executed under a
resource-constrained partial-Freebase setting. It is not a direct reproduction
of the paper's full-Freebase results, because the original system assumes a
large local Freebase deployment that was not available for this seminar setup.

## Two Experimental Layers

The work is organized into two layers:

1. **Infrastructure validation** checks whether the code, local KG service,
   SPARQL access, BM25 entity-name index, and benchmark format can work
   together.
2. **Formal partial-KG pilot** freezes a small WebQSP subset, builds an
   answer-independent partial graph, filters answerable questions, runs GoG,
   and reports the resulting score.

This distinction is important because the demo graph can validate the software
pipeline but should not be used as an accuracy result.

## Main Files

- [`Experiment/README.md`](../Experiment/README.md): experiment protocol and
  evaluation rules.
- [`Experiment/Formal Partial Experiment.md`](../Experiment/Formal%20Partial%20Experiment.md):
  formal pilot design, graph statistics, and score.
- [`Experiment/Results.md`](../Experiment/Results.md): compact result tables
  for infrastructure validation and formal evaluation.
- [`Experiment/Dataset analysis.md`](../Experiment/Dataset%20analysis.md):
  benchmark and dataset observations.
- [`Experiment/DEMO Pipeline Evidence.json`](../Experiment/DEMO%20Pipeline%20Evidence.json)
  and [`Experiment/Formal Pilot Evidence.json`](../Experiment/Formal%20Pilot%20Evidence.json):
  machine-readable evidence records.

## Seminar Takeaway

The main experimental contribution of this reimplementation is feasibility
rather than paper-level numerical reproduction. The repository demonstrates a
transparent small-scale route for running GoG with a partial Freebase graph,
while clearly reporting the graph size, retained questions, answerable
questions, and metric limitations.

