# Knowledge Graph
A knowledge graph (KG) is a data model that structures information as an interconnected network of real-world entities 

Knowledge Graph = Entities + Relations + Triples


# KGQA

Question

↓

Knowledge Graph

↓

Answer

Traditional Knowledege Graph Question Answering (KGQA) assumes complete KGs, where all factual triples required for each question are entirely covered by the given KG.

# Large Language Models
Large Language Models (LLM) have made great success in various natural language processing (NLP) tasks.

Advantages:
- Rich world knowledge
- Strong reasoning ability

However, LLMs still suffer from insufficient knowledge and hallucination issues.

Limitations:
- Hallucination
- Lack of explainability

These works can be roughly divided into two categories:

### (1) Semantic Parsing

Idea:
Convert natural language questions into graph queries.

Examples:
- KB-BINDER
- ChatKBQA

Limitation:
Strong dependence on complete KG structure.

### (2) Retrieval-Based Methods

Idea:
Retrieve relevant subgraphs.

Examples:
- ToG
- RoG
- StructGPT

Limitation:
Cannot recover missing knowledge.


# Generate-on-Graph
Treat LLM as an agent exploring the given KGs to retrieve relevant triples.

As a KG to generate additional factual triples.

`Retrieval + Generation`

Key difference:
Generate missing triples when retrieval fails.

# Contributions
 
Purpose leveraging LLMs for QA under incompleter KG (IKGQA) to better evaluate LLMs' ability, and construct corresponding IKGQA datasets based on existing KGQA dataset.

Propose GoG, which uses the Think-Searching-Generating framewwork, to address IKGQA.

Experimental results on two datasets show the superiority of GoG, and demonstrate that LLMs can be combined with incomplete KGs to answer complex questions.
