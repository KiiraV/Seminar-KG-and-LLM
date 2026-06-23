# GoG Partial-Freebase Engineering Package

This directory contains the engineering additions used with the official GoG
repository. Copy its contents into the root of a clean GoG checkout while
preserving the directory structure.

```text
gog_partial_setup/
├── .env.example
├── Makefile.partial
├── docker-compose.virtuoso.yml
├── requirements.partial.txt
└── scripts_partial/
```

The upstream repository remains the source of the GoG reasoning code:
https://github.com/YaooXu/GoG

## Installation

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -r requirements.partial.txt
.venv/bin/python -m spacy download en_core_web_lg
cp .env.example .env
```

Edit `.env` locally and never commit the API key.

## Execution Order

1. `extract_seed_mids.py`
2. `build_partial_freebase.py`
3. Start Virtuoso and import `FilterFreebase`
4. `test_sparql.py`
5. `check_answerability.py`
6. `build_bm25_partial.py`
7. Start `src/bm25_name2ids.py`
8. Run `src/GoG.py`

The non-LLM demo can also be rerun with:

```bash
make -f Makefile.partial demo
```

The target writes a JSON evidence manifest containing counts, strict question
IDs, and SHA-256 hashes.

`build_demo_partial_from_dataset.py` is only for infrastructure testing. It
uses gold benchmark triples and is invalid for model evaluation.

Use `check_answerability.py --mode sparql` for formal filtering. This executes
the benchmark gold SPARQL and confirms that at least one returned value matches
a recorded gold answer. `--mode entity-coverage` is only a diagnostic.

