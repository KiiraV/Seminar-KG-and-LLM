# Generate-on-Graph Reimplementation

This repository documents a seminar study and resource-constrained
reimplementation of:

> Yao Xu et al. *Generate-on-Graph: Treat LLM as both Agent and KG for
> Incomplete Knowledge Graph Question Answering*. EMNLP 2024.

The project analyzes the GoG method, maps the paper to the official code, and
evaluates a small WebQSP pilot on a partial Freebase graph.

## Scope

The original implementation assumes a local Virtuoso deployment containing
Freebase. A full deployment was outside the available hardware budget, so this
project uses two clearly separated tracks:

1. **Engineering validation:** a small graph built from benchmark-provided
   triples verifies Docker, Virtuoso, SPARQL, BM25, and the GoG interfaces.
   Because this graph contains gold information, it is not used for scoring.
2. **Formal pilot:** question IDs are frozen before an independent one-hop
   graph is retrieved from QLever Freebase. Only questions answerable on that
   graph are evaluated.

This is a resource-constrained reimplementation, not a numerical reproduction
of the paper's full-Freebase experiment.

## Recorded result

| Measurement | Value |
|---|---:|
| Frozen WebQSP questions | 10 |
| Resource-eligible questions | 9 |
| Answerable questions | 6 |
| Model graph | 47,523 triples / 4,536 entities |
| BM25 index | 12,640 names |
| Model | Qwen2.5 7B via Ollama |
| Relaxed answer match | 2/6 (33.3%) |
| Coverage-adjusted result | 2/10 (20.0%) |

The six-question result demonstrates that the complete workflow can be run and
audited. It is too small to estimate full WebQSP performance or to compare
directly with the paper's reported scores.

## Repository guide

| Path | Content |
|---|---|
| [`Reimplementation/README.md`](Reimplementation/README.md) | Entry point for setup, architecture, limitations, and reproducibility evidence |
| [`Reimplementation/formal_partial_experiment/`](Reimplementation/formal_partial_experiment/) | Lightweight formal-pilot scripts and recorded result evidence |
| [`Experiment/README.md`](Experiment/README.md) | Experimental protocol and reporting rules |
| [`Experiment/Formal Partial Experiment.md`](Experiment/Formal%20Partial%20Experiment.md) | Formal pilot design and result |
| [`Report/Seminar report.md`](Report/Seminar%20report.md) | English seminar report draft |
| [`notes/`](notes/) | Paper-reading notes |
| [`Reference/Paper 4-Generate on Graph.pdf`](Reference/Paper%204-Generate%20on%20Graph.pdf) | Paper used for the seminar |

## Reproducing the setup

Clone the official GoG implementation separately:

```bash
git clone https://github.com/YaooXu/GoG.git
cd GoG
```

Then follow:

- [`Reimplementation/Partial Setup Guide.md`](Reimplementation/Partial%20Setup%20Guide.md)
- [`Reimplementation/Formal Pilot Guide.md`](Reimplementation/Formal%20Pilot%20Guide.md)
- [`Reimplementation/Freebase Setup.md`](Reimplementation/Freebase%20Setup.md)

This documentation repository intentionally does not store generated Virtuoso
databases, model weights, large RDF files, API credentials, or local absolute
paths. Commands use paths relative to the root of a GoG checkout.

## Evidence

Machine-readable summary files are available in:

- [`Experiment/DEMO Pipeline Evidence.json`](Experiment/DEMO%20Pipeline%20Evidence.json)
- [`Experiment/Formal Pilot Evidence.json`](Experiment/Formal%20Pilot%20Evidence.json)
- [`Reimplementation/formal_partial_experiment/results/experiment_evidence.json`](Reimplementation/formal_partial_experiment/results/experiment_evidence.json)

The formal pilot evidence can be printed locally with:

```bash
cd Reimplementation
./show_formal_result.sh
```

See the [reproduction audit](Reimplementation/Reproduction%20Audit.md) for the
claim boundary and known limitations.

## Sources

- [GoG paper on arXiv](https://arxiv.org/abs/2404.14741)
- [Official GoG implementation](https://github.com/YaooXu/GoG)
- [Google Freebase data dumps](https://developers.google.com/freebase)
- [QLever Freebase endpoint](https://qlever.dev/freebase)
