# Challenges and Resolutions

This document records the major technical challenges encountered during the reimplementation of the Generate-on-Graph (GoG) framework, the investigation process, and the final solutions adopted.

---

## Issue 1: Understanding the Original Infrastructure Requirements

### Problem

At the beginning of the reimplementation, it was unclear whether the provided code could be executed directly using the released repository.

After examining the paper and source code, it became evident that GoG does not operate solely as an LLM-based reasoning system. Instead, it relies heavily on a locally deployed Freebase Knowledge Graph accessed through Virtuoso SPARQL endpoints.

The repository documentation assumes that:

* A Freebase dump is already available.
* Virtuoso is already installed.
* A SPARQL endpoint is already running.

However, these prerequisites were not available in my local environment.

### Investigation

I first reviewed:

* The official GitHub repository.
* The project README.
* The deployment instructions.
* Relevant Virtuoso documentation.

I also inspected the retrieval modules to understand how the KG was queried during reasoning.

### Outcome

The first major realization was that reproducing GoG requires reproducing not only the codebase but also the underlying knowledge graph infrastructure.

---

## Issue 2: Freebase Data Availability

### Problem

The paper uses Freebase as the underlying knowledge graph.

However, Freebase is no longer actively maintained and the original Google Freebase API has been discontinued.

While historical Freebase dumps still exist, obtaining an appropriate dataset and identifying the exact version used in the paper proved challenging.

### Investigation

Several potential sources were explored:

* Official Freebase archive references
* Community-maintained mirrors
* Existing KGQA repositories using Freebase

The available resources often differed in format, completeness, or documentation quality.

### Outcome

A suitable Freebase dump was eventually located, but additional preprocessing was required before deployment.

---

## Issue 3: Full Freebase Deployment Feasibility

### Problem

The original GoG implementation assumes deployment of the complete Freebase dump.

The full dataset contains approximately:

* 1.9 billion RDF triples
* ~22 GB compressed
* > 250 GB uncompressed

Importing and indexing such a dataset requires substantial storage, memory, and processing time.

### Investigation

Several deployment options were considered:

1. Full Freebase deployment.
2. Partial dataset deployment.
3. Remote SPARQL endpoint alternatives.
4. Simplified testing environments.

The feasibility of each option was evaluated with respect to available hardware resources and project time constraints.

### Outcome

Full deployment was determined to be impractical within the available resources.

---

## Issue 4: Virtuoso Configuration and Deployment

### Problem

The GoG retrieval module depends on a functioning Virtuoso SPARQL endpoint.

Setting up Virtuoso required:

* Installation of the database system.
* Configuration of local services.
* RDF import procedures.
* SPARQL endpoint verification.

The deployment process involved several configuration steps not fully documented in the original repository.

### Investigation

Virtuoso documentation and community resources were consulted.

Multiple deployment attempts were performed before the endpoint became operational.

### Outcome

A local Virtuoso instance was successfully configured and validated through SPARQL test queries.

---

## Issue 5: Choosing a Reimplementation Strategy

### Problem

After discussing the deployment limitations, it became necessary to determine how the system could still be reproduced meaningfully without the complete Freebase infrastructure.

### Discussion with Tutor

I contacted the seminar tutor regarding the deployment constraints.

The recommendation was:

* Deploy a local Virtuoso endpoint.
* Use a partial Freebase dump if full deployment is infeasible.
* Restrict evaluation to benchmark questions answerable within the partial KG.

### Outcome

The reproduction strategy was adjusted accordingly.

Instead of reproducing the entire benchmark, the focus shifted to reproducing the reasoning workflow and validating the system behavior on a reduced but representative subset of knowledge graph data.

---

## Issue 6: Reproducibility vs. Practicality

### Observation

This experience highlighted an important challenge in reproducing KGQA systems.

Although the GoG framework itself is conceptually straightforward, the surrounding infrastructure introduces significant practical barriers.

The primary difficulty was not understanding the algorithm, but reproducing the external dependencies required for execution.

### Reflection

The reimplementation demonstrates that infrastructure requirements can become a major reproducibility bottleneck in knowledge graph research.

Future work could improve reproducibility by:

* Providing smaller benchmark-specific KG subsets.
* Supporting alternative knowledge graphs such as Wikidata.
* Offering containerized deployment environments.
* Reducing dependence on large local knowledge graph installations.
