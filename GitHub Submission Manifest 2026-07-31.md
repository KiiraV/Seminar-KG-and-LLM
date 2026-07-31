# GitHub Submission Manifest - 31 July 2026

This manifest defines the clean code-submission subset for the seminar
repository. It should be used when preparing the final GitHub upload.

## Required top-level files

- `README.md`
- `.gitignore`
- `Code Submission Note 2026-07-31.md`
- `Final Submission Checklist 2026-07-31.md`

## Required reimplementation files

- `Reimplementation/README.md`
- `Reimplementation/Architecture.md`
- `Reimplementation/Code Structure Analysis.md`
- `Reimplementation/Environment.md`
- `Reimplementation/Formal Pilot Guide.md`
- `Reimplementation/Freebase Setup.md`
- `Reimplementation/Issues.md`
- `Reimplementation/Partial Setup Guide.md`
- `Reimplementation/Reproduction Audit.md`
- `Reimplementation/Reproduction Checklist.md`
- `Reimplementation/Results.md`
- `Reimplementation/show_formal_result.sh`
- `Reimplementation/gog_formal_setup/`
- `Reimplementation/gog_partial_setup/`
- `Reimplementation/formal_partial_experiment/`

## Required experiment files

- `Experiment/README.md`
- `Experiment/Dataset analysis.md`
- `Experiment/Formal Partial Experiment.md`
- `Experiment/Results.md`
- `Experiment/DEMO Pipeline Evidence.json`
- `Experiment/Formal Pilot Evidence.json`

## Recommended report support files

- `Report/Appendix Reimplementation Addendum 2026-07-31.tex`
- `Report/Verified YOUR_thesis BibTeX No Google 2026-07-31.bib`
- final submitted report PDF, if the seminar platform allows storing it in GitHub

## Optional background files

- `notes/`
- `Reference/Paper 4-Generate on Graph.pdf`, only if redistribution is allowed

## Do not upload

- `.DS_Store`
- `.env`
- `.venv/`
- generated Virtuoso database files
- full or partial RDF dumps (`*.nt`)
- BM25 pickle files (`*.pkl`)
- model weights or Docker volumes
- TeX build artifacts (`*.aux`, `*.log`, `*.out`, `*.toc`, `*.bbl`, `*.blg`)
- old draft/support documents containing local absolute paths

The following old draft/support files currently contain local absolute paths and
should not be part of the final public GitHub upload unless cleaned:

- `Report/Final Seminar Closeout 2026-07-16.md`
- `Report/Seminar Live Demo Runbook.md`
- `Report/Draft Paper for Peer Review.md`
- `Report/Draft Paper for Peer Review v2.md`
- `Report/Draft Paper for Peer Review v3 Natural Rhythm.md`

## Minimal verification command

After upload, the most direct check is:

```bash
cd Reimplementation
./show_formal_result.sh
```

Expected summary:

```text
frozen_questions: 10
resource_eligible_questions: 9
gold_sparql_answerable_questions: 6
model_entities: 4536
model_triples: 47523
bm25_names: 12640
correct: 2
evaluated: 6
relaxed_answer_match: 0.333
```
