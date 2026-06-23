## Local Environment

- Device: MacBook Air M4
- Editor: VSCode
- Python environment: project-local `.venv` using Python 3.9
- KG database: Virtuoso running through Docker
- GoG workspace:

```text
/Users/kiira/Documents/Codex/2026-06-17/readme-md-https-github-com-yaooxu/GoG
```

## Required Services

The project uses two isolated service groups:

1. Engineering demo: Virtuoso 18890 and BM25 18891.
2. Formal pilot: Virtuoso 18892, BM25 18893, and Ollama 11434.

Example `.env`:

```bash
SPARQLPATH=http://127.0.0.1:18890/sparql
base_url=https://api.openai.com/v1
opeani_api_keys=replace_with_api_key
```

The formal pilot does not require a paid API key. Runtime variables point the
OpenAI-compatible client to Ollama:

```bash
base_url=http://127.0.0.1:11434/v1
opeani_api_keys=ollama
SPARQLPATH=http://127.0.0.1:18892/sparql
BM25_SERVICE_URL=http://127.0.0.1:18893/name2ids
```

## Verified Ports

| Service | URL | Status |
|---|---|---|
| Virtuoso SPARQL | `http://127.0.0.1:18890/sparql` | Verified |
| BM25 name-to-ID | `http://127.0.0.1:18891/name2ids` | Verified |
| Formal Virtuoso | `http://127.0.0.1:18892/sparql` | Verified |
| Formal BM25 | `http://127.0.0.1:18893/name2ids` | Verified |
| Ollama OpenAI API | `http://127.0.0.1:11434/v1` | Verified |

Port 18890 is used because port 8890 was already occupied locally.

## Secret Handling

The local `.env` is excluded from Git. Only `.env.example` is committed.
Any external API key must remain local and must not be pasted into the report,
screenshots, commits, or presentation. The recorded pilot used a local dummy
Ollama key rather than an external secret.
