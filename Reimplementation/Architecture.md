# Engineering Architecture

## System Components

```mermaid
flowchart LR
    D["WebQSP JSON"] --> F["Freeze 10 question IDs"]
    F --> S["Answer-free topic MID manifest"]
    QL["QLever Freebase"] --> X["One-hop extractor"]
    S --> X
    X --> C["Degree cap: 10,000"]
    C --> V["Formal Virtuoso :18892"]
    V --> A["Gold-SPARQL answerability"]
    A --> M["6 retained questions"]
    M --> G["Enriched model graph"]
    G --> B["BM25: 12,640 names"]
    B --> N["Name-to-ID :18893"]
    V --> E["GoG FreeBaseEnv"]
    N --> E
    L["Ollama + Qwen2.5 7B"] --> E
    E --> R["Predictions + 2/6 result"]
```

## Reproduction Workflow

```mermaid
flowchart TD
    A["Freeze benchmark subset"] --> B["Export topic MIDs only"]
    B --> C["Retrieve one-hop graph from QLever"]
    C --> D["Start and load Virtuoso"]
    D --> E{"SPARQL smoke test passes?"}
    E -- "No" --> D
    E -- "Yes" --> F["Filter answerable questions"]
    F --> G["Build BM25 name index"]
    G --> H{"Name-to-ID test passes?"}
    H -- "No" --> G
    H -- "Yes" --> I["Start local Ollama model"]
    I --> J["Run GoG"]
    J --> K["Evaluate and archive artifacts"]
```

## GoG Runtime Sequence

```mermaid
sequenceDiagram
    participant CLI as GoG.py
    participant Env as FreeBaseEnv
    participant LLM as LLM API
    participant KG as Virtuoso/SPARQL
    participant BM25 as Name-to-ID service

    CLI->>Env: initialize(question, topic entities)
    CLI->>LLM: request Thought and Action
    alt Search action
        Env->>BM25: resolve generated entity name
        BM25->>KG: query candidate entity types
        BM25-->>Env: candidate MID and types
        Env->>KG: retrieve neighboring triples
        Env->>LLM: filter relevant relations
        Env-->>CLI: observation triples
    else Generate action
        Env->>Env: select observed triples with BM25
        Env->>LLM: generate candidate triples
        Env->>LLM: verify candidates
        Env-->>CLI: generated observation
    end
    CLI->>LLM: continue or Finish[answer]
    CLI->>CLI: write JSONL, JSON, and log files
```

## Source-Code Mapping

| Concern | Upstream file | Local engineering addition |
|---|---|---|
| Main agent loop | `src/GoG.py` | partial benchmark CLI command |
| Search and generation | `src/environment.py` | unchanged |
| Freebase access | `src/kb_interface/freebase_func.py` | Dockerized Virtuoso |
| Entity linking | `src/bm25_name2ids.py` | small-graph BM25 builder |
| LLM access | `src/llms/interface.py` | `.env.example` |
| Dataset preparation | upstream processed JSON | seed and answerability scripts |
| KG deployment | upstream manual setup | Docker Compose |
| Run documentation | upstream README | `RUN_PARTIAL.md` |
| Formal graph extraction | not provided | QLever one-hop extractor |
| Resource control | not provided | answer-independent degree cap |
| Local model runtime | OpenAI API assumed | Ollama + Qwen2.5 7B |
| Evaluation robustness | `src/evaluate.py` | zero-division fix and metric audit |

## Artifact Boundaries

```mermaid
flowchart LR
    A["Demo KG from gold triples"] --> B["Infrastructure evidence"]
    C["Independent partial Freebase"] --> D["Formal experiment evidence"]
    B -. "must not become" .-> D
```

The demo path proves that services and interfaces work. Only the independent
partial-Freebase path can support a reported model score.

## Dual-Track Reproduction

```mermaid
flowchart TD
    U["Official GoG repository"] --> A["Track A: engineering validation"]
    U --> B["Track B: formal pilot"]
    A --> A1["Gold-derived 20-question demo"]
    A1 --> A2["Docker, SPARQL, BM25, interfaces"]
    B --> B1["Frozen WebQSP subset"]
    B1 --> B2["Independent QLever graph"]
    B2 --> B3["6-question Qwen2.5 7B run"]
    A2 --> C["Software correctness evidence"]
    B3 --> D["Experimental evidence: 2/6"]
```
