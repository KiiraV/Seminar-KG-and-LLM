# Introduction

## Motivation

Knowledge graphs provide explicit and structured factual knowledge, while
large language models provide flexible reasoning and broad internal knowledge.
Combining them can reduce hallucination and improve explainability.

Conventional KGQA assumes that every triple on the answer path exists in the
graph. In this setting, an LLM mainly acts as a controller that finds an answer
already stored in the KG. Real knowledge graphs are incomplete, so this
assumption hides an important failure mode.

## Research Gap

If a crucial triple is missing:

- semantic parsing may produce a valid query that returns no answer;
- retrieval-based systems cannot retrieve knowledge that is absent;
- an LLM-only system may answer from memory but hallucinate.

## Research Question

Can an LLM combine retrieved graph evidence with internal knowledge to answer
complex questions when the knowledge graph is incomplete?

## GoG Hypothesis

An LLM should play two roles:

1. **Agent:** plan, explore the KG, filter relations, and decide when to stop.
2. **Knowledge source:** generate and verify a missing factual triple when
   retrieval is insufficient.

## Contributions

The paper:

1. formulates Incomplete Knowledge Graph Question Answering (IKGQA);
2. constructs incomplete variants of WebQSP and CWQ;
3. proposes the training-free Thinking-Searching-Generating framework;
4. demonstrates stronger performance than retrieval-only baselines under
   incomplete-KG settings.

