# Partial-Freebase Engineering Guide

This guide describes the engineering-validation track used with a separate
checkout of the [official GoG repository](https://github.com/YaooXu/GoG).
The reusable additions are published in
[`gog_partial_setup/`](gog_partial_setup/).

## Required components

- Python 3.9 virtual environment
- Docker Desktop and Docker Compose
- OpenLink Virtuoso
- GoG dependencies and `en_core_web_lg`
- A partial RDF graph named `FilterFreebase`
- A BM25 name-to-MID index built from the same graph

Use paths relative to the root of your GoG checkout:

```text
GoG/
├── Freebase/virtuoso-opensource/database/FilterFreebase
├── Freebase/bm25.pkl
├── data/webqsp_partial/
└── src/
```

## Execution order

1. Select a small WebQSP subset.
2. Extract seed MIDs.
3. Build the demo RDF graph.
4. Start Virtuoso and import `FilterFreebase`.
5. Verify the SPARQL endpoint.
6. Run the strict gold-SPARQL answerability diagnostic.
7. Build the BM25 index from the imported graph.
8. Start the name-to-ID service.
9. Verify the GoG environment and interfaces.

Copy the reusable package into the root of a clean GoG checkout:

```bash
cp -R /path/to/Seminar-KG-and-LLM/Reimplementation/gog_partial_setup/. \
  /path/to/GoG/
cd /path/to/GoG
```

Example environment setup:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -r requirements.partial.txt
.venv/bin/python -m spacy download en_core_web_lg
cp .env.example .env
make -f Makefile.partial demo
```

Edit `.env` locally if an external model endpoint is used. Never commit API
credentials.

## Validity boundary

The engineering demo uses benchmark-provided crucial triples. It is useful for
testing software integration, but it contains gold information and must not be
used to report model accuracy.

Entity coverage and answerability are also different:

- **Entity coverage:** topic and answer entities occur somewhere in the graph.
- **Strict answerability:** executing the benchmark SPARQL query returns a
  recorded gold answer.

The verified demo produced 20/20 entity coverage but only 6/20 strict
answerability. Neither number is a model-performance score.

## Related documentation

- [Freebase setup](Freebase%20Setup.md)
- [Architecture](Architecture.md)
- [Reusable engineering package](gog_partial_setup/)
- [Reproduction checklist](Reproduction%20Checklist.md)
- [Reproduction audit](Reproduction%20Audit.md)
