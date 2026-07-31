# Reproduction Checklist

## Repository and Environment

- [x] Clone the official GoG repository.
- [x] Create a Python 3.9 virtual environment.
- [x] Install upstream and supplemental dependencies.
- [x] Install `en_core_web_lg`.
- [x] Add `.env.example` and ignore `.env`.
- [x] Confirm `GoG.py --help` runs.

## Knowledge Graph Services

- [x] Add Docker Compose for Virtuoso.
- [x] Expose SPARQL on port 18890.
- [x] Import the demo `FilterFreebase`.
- [x] Verify a SPARQL entity-name query.
- [x] Build the small-graph BM25 index.
- [x] Verify the name-to-ID endpoint on port 18891.

## Dataset Pipeline

- [x] Select the first 20 WebQSP IKG-20% examples for plumbing validation.
- [x] Extract 124 seed MIDs.
- [x] Generate and import the 217-triple demo KG.
- [x] Produce a 20-question entity-coverage diagnostic.
- [x] Execute gold SPARQL and retain the strict 6/20 demo subset.
- [x] Freeze the formal question IDs.
- [x] Use the independent QLever Freebase endpoint.
- [x] Build the formal one-hop partial graph.
- [x] Re-run answerability filtering.
- [x] Record the formal retention rate.

## Model Run

- [x] Start local Ollama instead of requiring an external API key.
- [x] Record Qwen2.5 7B and the run date.
- [x] Start the formal BM25 service on port 18893.
- [x] Run GoG with one process.
- [x] Archive JSONL predictions, JSON output, and logs.
- [x] Compute retained-set and coverage-adjusted accuracy.
- [x] Classify representative failure cases.

## Reporting Guardrails

- [x] Label the current 20-question graph as demo-only.
- [x] Do not report 20/20 coverage or 6/20 demo execution as model performance.
- [x] Replace final pilot fields only after an independent graph and recorded model run.
- [x] Report selected count, retained count, and graph policy with every score.
