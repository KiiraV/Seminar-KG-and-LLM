# Results

## Infrastructure Validation

| Check | Result |
|---|---|
| Python imports | Passed |
| spaCy `en_core_web_lg` vectors | Passed |
| Virtuoso startup | Passed |
| SPARQL query | Passed |
| Demo graph import | 217 triples |
| Entity-coverage diagnostic | 20/20 demo questions |
| Strict gold-SPARQL filter | 6/20 demo questions |
| BM25 index | 123 names |
| Name-to-ID query | `Samuel Taylor Coleridge -> m.078w2` |

These are engineering validation results, not model evaluation results.

## Formal Evaluation

| Dataset | Selected | Answerable | Retention | Model | Hits@1/EM |
|---|---:|---:|---:|---|---:|
| WebQSP pilot | 10 frozen / 9 resource eligible | 6 | 60.0% frozen / 66.7% eligible | Qwen2.5 7B | 33.3% relaxed match |

The upstream evaluator names this metric `Exact Match`, but its implementation
uses normalized substring overlap. The score is therefore reported as relaxed
answer match. This pilot is not directly comparable with the paper.
