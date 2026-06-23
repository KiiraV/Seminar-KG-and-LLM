# Method

## Overall Framework

GoG follows an iterative Thought-Action-Observation loop:

```text
Question and topic entities
        |
        v
Thinking -> Search or Generate -> Observation
        ^                           |
        +---------------------------+
                    |
                    v
              Finish[answer]
```

## Thinking

The LLM decomposes the question, identifies the next information need, and
chooses one of three actions:

- `Search[entity]`
- `Generate[sub-question]`
- `Finish[answer]`

## Searching

1. Link the entity name to a Freebase MID.
2. Retrieve one-hop relations and triples through SPARQL.
3. Ask the LLM to retain relations relevant to the current thought.
4. Add the selected triples to the reasoning context.
5. Expand to two hops after `Finish[unknown]` when allowed.

## Generating

1. Select relevant observed triples with BM25.
2. Ask the LLM to generate missing factual triples.
3. Optionally generate multiple candidates through self-consistency.
4. Ask the LLM to verify and retain plausible candidates.

## Entity Linking

For a newly generated entity name:

1. retrieve similar names from a BM25 index;
2. query candidate entity types from Freebase;
3. ask the LLM to select the contextually correct MID.

## Termination

GoG stops when the model emits `Finish[answer]`, or falls back to an LLM-only
answer after exhausting the bounded reasoning loop.
