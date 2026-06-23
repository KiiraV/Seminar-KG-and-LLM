# Reimplementation

This directory documents the resource-constrained reproduction of GoG. Start
with the architecture and then choose the engineering or formal track.

## Reading order

1. [Architecture](Architecture.md)
2. [Freebase setup](Freebase%20Setup.md)
3. [Partial-Freebase engineering guide](Partial%20Setup%20Guide.md)
4. [Formal pilot guide](Formal%20Pilot%20Guide.md)
5. [Code structure analysis](Code%20Structure%20Analysis.md)
6. [Environment](Environment.md)
7. [Results](Results.md)
8. [Issues and limitations](Issues.md)
9. [Reimplementation checklist](Reimplementation%20Checklist.md)
10. [Reimplementation audit](Reimplementational%20Audit.md)

## Two-track design

| Track | Purpose | Can support a model score? |
|---|---|---|
| Engineering demo | Verify Docker, Virtuoso, SPARQL, BM25, and GoG interfaces | No, because the graph uses benchmark crucial triples |
| Formal pilot | Evaluate GoG on an independently retrieved partial graph | Yes, but only as a six-question pilot |

## What is available

- Architecture and data-flow diagrams
- Environment and service configuration
- Graph-construction and filtering protocol
- Reusable Docker Compose, Makefile, and Python setup packages
- Machine-readable experiment summaries in `../Experiment/`
- Code-to-paper mapping
- Known implementation corrections and limitations

## What is not available

Large or machine-specific artifacts are intentionally excluded:

- complete or partial RDF dumps;
- Virtuoso database files;
- model weights and container volumes;
- API keys and `.env` files;
- absolute paths from the original computer.

The official reasoning implementation remains available from
[YaooXu/GoG](https://github.com/YaooXu/GoG).

