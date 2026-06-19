# Experimental Results

## Original Paper Results

The authors compare GoG against:

- ToG
- RoG
- StructGPT
- ChatKBQA

GoG consistently achieves the best performance under incomplete KG settings.

## Key Observation

Performance improvement becomes more significant as the incompleteness level increases.

This indicates that the Generate module effectively compensates for missing graph knowledge.

## My Observation

The reproduced system successfully completed retrieval and generation workflows.

Generated triples helped recover reasoning paths that would otherwise be unavailable.
