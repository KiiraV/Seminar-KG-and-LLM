# Formal Partial-Freebase Experiment

This directory is independent from the gold-derived engineering demo.
It builds a small Freebase graph from the public QLever Freebase endpoint:

<https://qlever.dev/freebase>

The graph-construction stage reads only frozen question IDs and topic MIDs. It
does not read benchmark answers, gold SPARQL, `mid_crucial_triples`, or
`crucial_triples`.

## Scientific protocol

1. Freeze the first ten WebQSP examples in benchmark order.
2. Write a separate seed manifest containing only question IDs and topic MIDs.
3. Retrieve outgoing and incoming one-hop Freebase triples for those MIDs from
   QLever.
4. Retrieve names, aliases, and types for entities appearing in the one-hop
   graph.
5. Import the extracted graph into an isolated Virtuoso container on port
   `18892`.
6. Execute gold SPARQL only after graph construction to measure answerability.
7. Build a separate BM25 index and run GoG only on the retained questions.

The use of gold SPARQL in step 6 is evaluation, not graph construction.

## Files

- `data/frozen_questions.json`: evaluation records, including answers.
- `data/graph_seeds.json`: answer-free input to graph extraction.
- `data/FormalFreebase.nt`: independently retrieved partial graph.
- `data/answerable_questions.json`: retained evaluation population.
- `data/bm25_formal.pkl`: entity-linking index for the same graph.
- `results/`: model predictions and experiment evidence.

## Commands

```bash
make -f Makefile.formal freeze
make -f Makefile.formal extract
make -f Makefile.formal import
make -f Makefile.formal filter
make -f Makefile.formal model-graph
make -f Makefile.formal model-import
make -f Makefile.formal bm25
```

Start the formal BM25 service in a separate terminal:

```bash
make -f Makefile.formal name-service
```

Then run the preflight:

```bash
make -f Makefile.formal preflight
```

The recorded pilot uses local Ollama with `qwen2.5:7b`. Ensure the Ollama
container and model are available:

```bash
docker run -d --name gog-ollama -p 11434:11434 \
  -v gog-ollama-models:/root/.ollama ollama/ollama:latest
docker exec gog-ollama ollama pull qwen2.5:7b
```

The final model run is intentionally separate:

```bash
make -f Makefile.formal run
```

## Interpretation

This is a pilot experiment, not a paper-scale reproduction. Report both:

- retention: answerable frozen questions / all frozen questions;
- model accuracy: correct predictions / answerable frozen questions.

Do not compare the resulting accuracy directly with the paper's full benchmark
score.
