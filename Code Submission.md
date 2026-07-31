# Code Submission

Repository:

https://github.com/KiiraV/Seminar-KG-and-LLM

## What This Repository Contains

This repository documents and packages a resource-constrained reimplementation
of the official GoG code for the seminar paper:

> Generate-on-Graph: Treat LLM as both Agent and KG for Incomplete Knowledge
> Graph Question Answering.

The original GoG implementation assumes access to a local Freebase deployment.
Since a full Freebase deployment was not feasible on the available local
hardware, the submitted code uses a partial-Freebase workflow and clearly
separates engineering validation from a small formal pilot.

## Main Entry Points

| Purpose | Path |
|---|---|
| Repository overview | `README.md` |
| Reimplementation overview | `Reimplementation/README.md` |
| Partial setup package | `Reimplementation/gog_partial_setup/` |
| Formal pilot package | `Reimplementation/gog_formal_setup/` |
| Formal pilot scripts and recorded outputs | `Reimplementation/formal_partial_experiment/` |
| Lightweight result display command | `Reimplementation/show_formal_result.sh` |
| Experiment protocol | `Experiment/README.md` |
| Formal result explanation | `Experiment/Formal Partial Experiment.md` |
| Machine-readable formal evidence | `Experiment/Formal Pilot Evidence.json` |
| Machine-readable demo evidence | `Experiment/DEMO Pipeline Evidence.json` |
| Code-to-paper mapping | `Reimplementation/Code Structure Analysis.md` |
| Reproduction audit | `Reimplementation/Reproduction Audit.md` |

## Reproduction Tracks

### Track A: Engineering Validation

The engineering demo verifies that Docker, Virtuoso, SPARQL, BM25, and the GoG
interfaces can communicate. This track uses benchmark-provided crucial triples
and is therefore not used for model scoring.

It validates the local infrastructure only.

### Track B: Formal Partial-Freebase Pilot

The formal pilot freezes question IDs before graph construction. It then builds
an independent one-hop Freebase graph from QLever using topic MIDs only.
Answers, gold SPARQL, and benchmark crucial triples are not used during graph
construction. Gold SPARQL is used only afterward to filter questions that remain
answerable on the partial graph.

## Recorded Formal Result

| Item | Value |
|---|---:|
| Frozen WebQSP questions | 10 |
| Resource-eligible questions | 9 |
| Gold-SPARQL answerable questions | 6 |
| Model graph triples | 47,523 |
| Model graph entities | 4,536 |
| BM25 names | 12,640 |
| Model | Qwen2.5 7B via Ollama |
| Correct predictions | 2 |
| Evaluated questions | 6 |
| Metric | Relaxed answer match |
| Score | 2/6 = 33.3% |

The upstream evaluator calls the metric `Exact Match`, but the implementation
accepts normalized substring overlap. For this reason, the result is reported as
relaxed answer match.

## Verified Local Command

The following command was rerun successfully on 31 July 2026 in the local demo
checkout. In the submitted repository, the same saved evidence can be inspected
with:

```bash
cd Reimplementation
./show_formal_result.sh
```

The script printed the saved formal-pilot evidence and per-question outcomes.

## What Is Not Included

The repository intentionally excludes:

- full Freebase dumps;
- generated Virtuoso database files;
- model weights and Docker volumes;
- API keys and `.env` files;
- local virtual environments;
- machine-specific absolute paths.

These files are excluded because they are either too large, machine-specific,
or sensitive. The repository instead stores scripts, setup packages, evidence
files, result summaries, and reproducibility documentation.

## Claim Boundary

This code submission supports a resource-constrained workflow reproduction. It
does not claim to reproduce the full benchmark results from the GoG paper.

The reproduced workflow covers:

```text
partial graph construction
  -> Virtuoso/SPARQL loading
  -> answerability filtering
  -> BM25 entity linking
  -> GoG reasoning
  -> prediction logging
  -> evaluation evidence
```
