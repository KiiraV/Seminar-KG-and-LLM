# GoG (Generate-on-Graph)
The paper related to GoG can be divided into three categories.

# Knowledge Graph Question Answering

A knowledge graph (KG) is a data model that structures information as an interconnected network of real-world entities 

Knowledge Graph = Entities + Relations + Triples


Traditional Knowledege Graph Question Answering (KGQA) assumes complete KGs, where all factual triples required for each question are entirely covered by the given KG.

Question

↓

Knowledge Graph

↓

Answer


# Large Language Models
Large Language Models (LLM) have made great success in various natural language processing (NLP) tasks.
Recent studies such as StructGPT, Think-on-Graph (ToG), and Reason-on-Graph (RoG) utilize LLMs to explore graph structures and perform reasoning.

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

# Contributions
 
Purpose leveraging LLMs for QA under incompleter KG (IKGQA) to better evaluate LLMs' ability, and construct corresponding IKGQA datasets based on existing KGQA dataset.

Propose GoG, which uses the Think-Searching-Generating framewwork, to address IKGQA.

Experimental results on two datasets show the superiority of GoG, and demonstrate that LLMs can be combined with incomplete KGs to answer complex questions.

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
