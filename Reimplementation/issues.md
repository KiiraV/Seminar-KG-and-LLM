# Issue 1

## Freebase Data Availability Update

The original Freebase download link may not be directly usable as a one-click dataset download. The Freebase API has been shut down, while Google still hosts the final historical Freebase data dumps at https://developers.google.com/freebase. The full Freebase triples are large, so reproducing the original setting requires deploying the dump locally with Virtuoso.

If the full dump cannot be deployed due to resource limits, a partial dump may be used. However, the benchmark must then be filtered to include only questions answerable by the deployed partial KG. Thus, the recommended workflow is:

1. Select a benchmark split.
2. Extract seed entities from the benchmark, including topic entities and gold answer MIDs/QIDs.
3. Construct a partial KG around these entities, including necessary 1-hop/2-hop triples and CVT nodes.
4. Import the partial KG into Virtuoso.
5. Verify each question against the local SPARQL endpoint.
6. Keep only questions whose gold answers are available in the partial KG.
7. Report the retained question count and mark results as partial-KG results.

Results from a partial dump are not directly comparable to the full Freebase setting used in the paper.
