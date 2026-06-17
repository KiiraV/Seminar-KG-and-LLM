# Knowledge Graphs and Large Language Models
# Generate-On-Graph: Treat LLM as both Agent and KG for Incomplete Knowledge Graph Question Answering

## Research Problem
Most KGQA systems assume a complete knowledge graph.
However, real-world knowledge graphs are often incomplete.
When important triples are missing, retrieval-based methods fail.

## Research Question
Can LLMs be combined with incomplete KGs to answer complex questions?

## Solution
`Generate-on-graph for IKGQA`

Utilises LLMs for QA under incomplete KG (IKGQA), to simulate realistic scenarios
Closer to real-world scenarios where the given KG is incomplete to answer users’ questions
Better evaluate the ability of LLMs to Integrate and external knowledge 

## Innovation 
`Thinking-Searching-Generating framework`

### (1) Thinking: 
LLMs decompose the question and determine whether to conduct further searches or generate relevant triples based on current state

### (2) Searching: 
LLMs use pre-defined tools to explore the KGs and filter out irrelevant triples

### (3) Generating: 
LLMs use its internal knowledge and reasoning abilities to generate required new factual triples based on explored subgraph and verify them

## Results
GoG outperforms retrieval-only methods such as ToG under incomplete KG settings.

## Limitation

Generated triples may be incorrect.
Verification also relies on the LLM itself.
