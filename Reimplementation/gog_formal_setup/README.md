# Reusable Formal-Pilot Package

This directory mirrors the engineering files used for the independent WebQSP
pilot. Copy it into a clean checkout of the official GoG repository.

## Included

- `Makefile.formal`: end-to-end orchestration;
- `docker-compose.formal.yml`: isolated Virtuoso on port 18892;
- `formal_partial_experiment/`: freezing, extraction, resource filtering,
  model-graph preparation, and result summarization;
- `upstream_compatibility.patch`: OpenAI 0.x/1.x compatibility, configurable
  BM25 paths and ports, retry termination, and zero-division-safe evaluation.

## Apply to a clean GoG checkout

```bash
cp -R formal_partial_experiment /path/to/GoG/
cp Makefile.formal docker-compose.formal.yml /path/to/GoG/
cd /path/to/GoG
git apply /path/to/upstream_compatibility.patch
```

The package also relies on the shared scripts in
`Reimplementation/gog_partial_setup/scripts_partial/`.

## Rebuild sequence

```bash
make -f Makefile.formal freeze
make -f Makefile.formal extract
make -f Makefile.formal resource-filter
make -f Makefile.formal filter
make -f Makefile.formal model-graph
make -f Makefile.formal model-import
make -f Makefile.formal bm25
make -f Makefile.formal name-service
make -f Makefile.formal preflight
make -f Makefile.formal run
```

QLever is a public service. Respect rate limits and retain the generated
one-hop checkpoint when rerunning metadata enrichment.
