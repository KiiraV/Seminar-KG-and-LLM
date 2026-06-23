# Generate-on-Graph Reimplementation

This repository documents a seminar study and resource-constrained
reimplementation of:

> Yao Xu et al. *Generate-on-Graph: Treat LLM as both Agent and KG for
> Incomplete Knowledge Graph Question Answering*. EMNLP 2024.

The project analyzes the GoG method, maps the paper to the official code, and
builds a locally runnable partial-Freebase pipeline with Docker, Virtuoso,
SPARQL, and BM25 entity linking.

## Reimplementation scope

The original system assumes a local Virtuoso deployment over Freebase. A full
deployment is not practical on the available laptop, so this project follows a
partial-KG protocol:

1. Select a WebQSP subset.
2. Extract topic and answer entity MIDs.
3. Build a partial Freebase graph around those seeds.
4. Load the graph into Virtuoso.
5. Retain only questions answerable by that graph.
6. Rebuild the BM25 entity-linking index.
7. Run GoG and report the retained set and model configuration.

This is a resource-constrained reimplementation, not a direct reproduction of
the paper's full-Freebase experiment.

## Current verified status

| Component | Status | Evidence |
|---|---|---|
| Python environment | Complete | All GoG imports and spaCy vectors load |
| Virtuoso in Docker | Complete | SPARQL endpoint responds on port 18890 |
| Dataset preprocessing | Complete | 124 seed MIDs extracted from 20 WebQSP examples |
| Demo partial KG | Complete | 217 triples imported |
| Entity-coverage diagnostic | Complete | 20/20 demo questions covered |
| Strict gold-SPARQL filter | Complete | 6/20 demo questions executable |
| BM25 index | Complete | 123 entity names indexed |
| Name-to-ID service | Complete | Successful typed MID response on port 18891 |
| Formal partial Freebase | Complete pilot | 47,523 triples independently retrieved from QLever |
| LLM inference | Complete pilot | Local Qwen2.5 7B via Ollama |
| Formal pilot result | Complete | 2/6 relaxed answer match |

The 20-question demo graph is built from benchmark-provided crucial triples.
It proves that the infrastructure works, but it contains gold information and
must not be reported as an experimental score.

## Repository guide

| Path | Content |
|---|---|
| [`Report/Seminar report.md`](Report/Seminar%20report.md) | Complete English report draft |
| [`Report/latex/`](Report/latex/) | Compile-ready LaTeX report template and bibliography |
| [`presentation/GoG_Seminar_Presentation.pptx`](presentation/GoG_Seminar_Presentation.pptx) | Rendered 12-slide English seminar deck |
| [`presentation/GoG_Seminar_Speaker_Script.pdf`](presentation/GoG_Seminar_Speaker_Script.pdf) | Print/iPad speaker manuscript with Q&A |
| [`presentation/Presentation Outline.md`](presentation/Presentation%20Outline.md) | English slide structure and speaking points |
| [`notes/`](notes/) | Paper-reading notes by section |
| [`Reimplementation/`](Reimplementation/) | Environment, Freebase setup, issues, and reproducibility status |
| [`Reimplementation/Code Structure Analysis.md`](Reimplementation/Code%20Structure%20Analysis.md) | Official code and local patch mapping |
| [`Experiment/`](Experiment/) | Dataset protocol and result templates |
| [`Experiment/Formal Partial Experiment.md`](Experiment/Formal%20Partial%20Experiment.md) | Independent pilot: 2/6 relaxed answer match |
| [`Reference/Paper.pdf`](Reference/Paper.pdf) | Official arXiv paper |
| [`Seminar Traceability Matrix.md`](Seminar%20Traceability%20Matrix.md) | Requirement-to-evidence mapping |
| [`Repository Maintenance.md`](Repository%20Maintenance.md) | Git and update workflow |
| [`Submission Readiness.md`](Submission%20Readiness.md) | Final claims, deliverables, and manual checks |
| [`Engineering Deliverables Audit.md`](Engineering%20Deliverables%20Audit.md) | Final audit of the assigned Codex engineering scope |

## Local execution

The executable GoG checkout is maintained next to this repository:

```text
/Users/kiira/Documents/Codex/2026-06-17/readme-md-https-github-com-yaooxu/GoG
```

Its end-to-end instructions are in `GoG/RUN_PARTIAL.md`. Secrets are stored
only in the local `GoG/.env` file and are not committed.

Engineering diagrams and the executable checklist are available in:

- [`Reimplementation/Architecture.md`](Reimplementation/Architecture.md)
- [`Reimplementation/Reproduction Checklist.md`](Reimplementation/Reproduction%20Checklist.md)
- [`Reimplementation/Reproduction Audit.md`](Reimplementation/Reproduction%20Audit.md)
- [`Reimplementation/gog_partial_setup/`](Reimplementation/gog_partial_setup/) contains the reusable engineering package.
- [`Reimplementation/gog_formal_setup/`](Reimplementation/gog_formal_setup/) contains the independent pilot package and upstream compatibility patch.

Run the dependency-free repository audit before each commit:

```bash
python3 tools/check_repository.py
```

Compile the report template with:

```bash
make -C Report/latex
```

## Research question

Can an LLM combine retrieved graph evidence with its internal knowledge to
answer complex questions when crucial KG triples are missing?

## Sources

- [GoG paper on arXiv](https://arxiv.org/abs/2404.14741)
- [Official GoG implementation](https://github.com/YaooXu/GoG)
- [Google Freebase data dumps](https://developers.google.com/freebase)
