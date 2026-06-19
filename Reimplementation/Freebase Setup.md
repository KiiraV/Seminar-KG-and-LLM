# Freebase Setup
## Original Setup Requirement
The original Generate-on-Graph implementation relies on a local deployment of the Freebase Knowledge Graph through Virtuoso.

`https://github.com/YaooXu/GoG/blob/main/README.md`

According to the authors, the system requires:

- Virtuoso Open Source 7.2.x
- Freebase RDF dump
- SPARQL endpoint
- Python-based retrieval modules

The retrieval component communicates directly with the local SPARQL endpoint during graph exploration.

## Challenges of Full Freebase Deployment
Deploying the complete Freebase dump presents significant practical challenges.

The original Freebase dataset contains approximately:

- 1.9 billion RDF triples
- 22 GB compressed size
- More than 250 GB uncompressed size

In addition to storage requirements, importing and indexing the data within Virtuoso requires substantial computational resources and processing time. Furthermore, many original Freebase resources are no longer actively maintained because the Freebase API has been discontinued.

## Reimplementation Decision
During reproduction and further examination, a full Freebase deployment was considered impractical for the available hardware resources.

Following discussions with the seminar tutor, the partial-KG strategy was adopted. Instead of importing the complete Freebase dump, only a subset of graph data relevant to the selected benchmark questions was retained. 

This approach allows the reasoning workflow of GoG to be reproduced while significantly reducing computational requirements.

## Local Deployment Procedure
The local deployment process consisted of:

1. Install Virtuoso Open Source 7.2.5.
2. Obtain the Freebase RDF dump.
3. Filter English triples.
4. Import RDF files into Virtuoso.
5. Build the SPARQL endpoint.
6. Verify query execution.

## Vaildation
After deployment, SPARQL queries were executed to verify that the local endpoint was functioning correctly.

Successful query execution confirmed that the retrieval module could communicate with the knowledge graph as required by GoG.

## Refletion
The deployment process revealed that infrastructure setup is one of the major barriers to reproducing KGQA systems.

Although the GoG framework itself is conceptually straightforward, the dependency on Freebase and Virtuoso significantly increases reproduction complexity.

Future implementations may benefit from replacing Freebase with more accessible alternatives such as Wikidata.
