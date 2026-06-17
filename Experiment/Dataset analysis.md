# Dataset Analysis: WebQSP and CWQ under Incomplete KG

## 1. Benchmark Overview
The Generate-on-Graph (GoG) framework is evaluated on two widely recognized Knowledge Graph Question Answering (KGQA) benchmarks, both of which utilize Freebase as the underlying knowledge source:

WebQuestionsSP (WebQSP): A dataset consisting of questions that are answerable through semantic parsing, primarily focusing on 1-hop and 2-hop reasoning paths.

Complex WebQuestion (CWQ): A more challenging benchmark built upon WebQuestions, requiring multi-hop reasoning, constraints, and compositions.

For the purpose of this seminar and to manage computational costs, the evaluation focuses on a randomly selected subset of 1,000 samples from these benchmarks.

## 2. Construction of the IKGQA Task
Unlike conventional KGQA, which assumes a complete Knowledge Graph (CKG), the Incomplete Knowledge Graph Question Answering (IKGQA) task simulates real-world scenarios where factual links are missing.

Incompleteness Simulation (Algorithm 1)

To construct the Incomplete Knowledge Graphs (IKGs), we follow the paper’s methodology of randomly dropping crucial triples from the Gold Relation Path:

Identify the gold relation path w 
g
​	
  for each question.

Apply a drop probability p (e.g., 20%, 40%, 60%, 80%) to each triple in the path.
Strict Deletion Rule: When a triple is dropped, all existing relations between those two entities are removed to ensure the model cannot "cheat" by finding an alternative edge, forcing the LLM to rely on its inherent knowledge.

## 3. Reimplementation Strategy: The Partial Dump
Due to significant technical obstacles and hardware limitations, this reimplementation utilizes a Partial Dump strategy rather than the full 250GB Freebase dataset.

Technical Obstacles

Access Constraints: The official Google Cloud Storage link for the full Freebase RDF dump (freebase-rdf-latest.gz) returned an 'Access Denied' error, as the public hosting has been restricted by the provider.

Hardware Limitations: Deploying the full Freebase instance via Virtuoso requires substantial memory (often >32GB RAM for indexing) and storage, which exceeds the specifications of the local MacBook Air M4 environment.
Extraction Methodology

To maintain the integrity of the experiment while working within these constraints, we followed the tutor's recommendation to extract an "answerable" subset:

Gold Path Extraction: We identified a subset of questions (e.g., 100 samples) and retrieved the triples belonging to their Gold Relation Paths from available repository fragments.

Neighborhood Retrieval: We extracted the immediate 1-hop and 2-hop neighbors for each Topic Entity in these questions to provide sufficient context for the Search and Generate actions.

Connectivity Verification: We ensured that before the simulation of incompleteness, the answer entities were reachable via SPARQL queries within our local Virtuoso Docker container.

## 4. Dataset Statistics
The following table provides the statistics for the subset used in this reimplementation:
Metric
WebQSP (Subset)
CWQ (Subset)
Number of Samples
[Your Count, e.g., 100]
[Your Count, e.g., 100]
Median Neighbor Nodes
~427
~26
Avg. Edges Deleted (IKG-40%)
~13.9
~4.3
Handling Isolated Entities
To ensure the Searching action can be initiated, we explicitly filtered out samples where the Topic Entity became isolated (degree = 0) after triple deletion. This ensures that the LLM agent always has at least one starting point to "Think" and "Search" before being forced to "Generate".

## 5. Supplementary Data: Wikidata Mapping

Where Freebase data was partially incomplete or missing mappings, we integrated Wikidata RDF patches as suggested in the setup documentation. This allows the model to map Freebase Machine Identifiers (MIDs) to Wikidata entities, enhancing the context available during the Verifying step of the Generate Action.
