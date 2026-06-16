# ToG (Think-on-Graph)
## Pros
- Utilizes structured knowledge from the knowledge graph.
- Provides interpretable reasoning paths.
- Reduces hallucinations compared to pure LLM prompting.
- Uses iterative graph exploration guided by the LLM.
- Does not require model fine-tuning.

## Cons
- Strongly depends on existing graph structure.
- Cannot recover missing knowledge when critical triples are absent.
- Performance drops significantly under incomplete KG settings.
- Retrieval quality directly affects final answers.
- Limited ability to leverage the LLM's internal knowledge.

# GoG (Generate-on-Graph)
## Pros
- Combines graph retrieval with knowledge generation.
- Can generate missing triples when retrieval fails.
- Better performance on incomplete knowledge graphs.
- Leverages both external KG knowledge and internal LLM knowledge.
- More robust than retrieval-only approaches.

## Cons
- Generated triples may be incorrect.
- Verification still relies on the LLM.
- Risk of hallucination and error propagation.
- Higher computational cost due to Search–Generate–Verify cycles.
- Performance is highly dependent on the underlying LLM quality.
