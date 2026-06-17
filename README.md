# Seminar-KG&LLM
## Paper Information
Title:
Generate-on-Graph: Treat LLM as both Agent and KG in Incomplete Knowledge Graph Question Answering

Research Area:
Knowledge Graphs and Large Language Models (KG&LLM)

Venue:
EMNLP 2024

---

## Project Objective

This seminar project aims to:

1. Understand the GoG framework and its motivation.
2. Analyze the official implementation provided by the authors.
3. Reproduce the main workflow and selected experiments.
4. Evaluate strengths, limitations, and potential improvements.

---

## Research Background

Knowledge Graph Question Answering (KGQA) systems traditionally rely on complete knowledge graphs. However, real-world knowledge graphs are often incomplete, causing retrieval-based methods to fail when crucial triples are missing.

GoG addresses this issue by allowing Large Language Models to act as both:

* An intelligent reasoning agent
* A dynamic knowledge source

The framework combines retrieval and generation to answer questions over incomplete knowledge graphs.

---

## Repository Structure

Seminar/

├── README.md

├── report/

├── presentation/

├── notes/

├── reproduction/

├── experiments/

└── figures/

---

## Current Progress

### Completed

* Paper fully reviewed
* Methodology analyzed
* Repository structure examined
* Freebase dependency identified
* Seminar notes organized

### Ongoing

* Code architecture analysis
* Reimplementation study
* Experiment preparation

### Pending

* Full pipeline execution
* Experimental evaluation
* Final report writing
* Presentation completion

---

## Reproduction Challenges

The official implementation depends on:

* Freebase Knowledge Graph
* Virtuoso SPARQL Endpoint
* BM25 Entity Linking Service
* OpenAI / Qwen APIs

One major challenge is that the original Freebase dump is no longer easily accessible through the links provided in the repository.

---

## Future Work

* Run selected experiments on CWQ and WebQSP datasets
* Compare GoG with retrieval-only approaches
* Analyze verification reliability
* Investigate alternative knowledge graph backends

---

## Author

Seminar: Knowledge Graphs and Large Language Models

Karlsruhe Institute of Technology (KIT)
