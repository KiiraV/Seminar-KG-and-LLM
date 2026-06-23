# Code Analysis

## Official Repository

https://github.com/YaooXu/GoG

## Main Execution Path

| File | Responsibility |
|---|---|
| `src/GoG.py` | CLI, dataset loading, reasoning loop, output, evaluation |
| `src/environment.py` | Search, Generate, Verify, relation filtering |
| `src/kb_interface/freebase_func.py` | SPARQL queries and graph conversion |
| `src/bm25_name2ids.py` | Entity-name retrieval and Flask service |
| `src/llms/interface.py` | LLM API abstraction |
| `src/evaluate.py` | Exact-match-style evaluation |
| `prompts_v2/` | Agent and primitive-task prompts |

## Runtime Flow

1. `GoG.py` loads a JSON benchmark.
2. It creates `FreeBaseEnv` with topic entities and the question.
3. The LLM emits a Thought and Action.
4. `FreeBaseEnv.step()` dispatches Search or Generate.
5. Search calls SPARQL and LLM relation filtering.
6. Generate calls BM25 triple selection and LLM generation/verification.
7. Each trace is written to a JSONL result file.
8. The JSONL file is converted to JSON and evaluated.

## Important Implementation Details

- The reasoning loop is bounded to six iterations.
- `Finish[unknown]` can trigger two-hop expansion.
- `mid_crucial_triples` are filtered from retrieved triples to simulate an
  incomplete KG.
- The upstream environment variable is misspelled as `opeani_api_keys`; local
  configuration must preserve this spelling.
- The original `gpt-3.5-turbo-0613` backbone is no longer available, so a
  modern run is a reimplementation rather than an exact model reproduction.

## External Services

- Virtuoso SPARQL endpoint: port 18890 in the local setup.
- BM25 name-to-ID Flask service: port 18891.
- OpenAI-compatible LLM endpoint: configured in `.env`.

## Local Additions

The local GoG checkout adds:

- `docker-compose.virtuoso.yml`;
- `.env.example`;
- `requirements.partial.txt`;
- `RUN_PARTIAL.md`;
- helper scripts under `scripts_partial/`.

These additions preserve the upstream reasoning code while making the
partial-Freebase infrastructure reproducible.
