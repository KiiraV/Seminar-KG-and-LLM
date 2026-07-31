# Final Submission Checklist

This checklist is for the final seminar submission of Paper 4:
Generate-on-Graph: Treat LLM as both Agent and KG for Incomplete Knowledge Graph Question Answering.

## 1. Report Submission

Use the Overleaf/LaTeX report as the final submitted report.

Before exporting the final PDF, apply the feedback from the peer review:

1. Add and compile real references.
2. Mention every figure and table in the text before or near where it appears.
3. Describe the local metric as "relaxed answer match", not strict "Exact Match".
4. Reduce length and remove unnecessary template pages if they are not required.
5. Make the language more personal and less uniformly polished.

Recommended final wording for the metric:

> The upstream evaluator names this metric Exact Match, but the implementation accepts normalized substring overlap between predicted and gold answers. I therefore report the local pilot result as relaxed answer match rather than strict exact match.

Recommended final wording for the reproduction boundary:

> This local experiment should be interpreted as workflow reproducibility under resource constraints. It verifies the chain from partial graph construction to Virtuoso/SPARQL access, BM25 entity linking, GoG reasoning, prediction logging, and evaluation. It does not reproduce the full-Freebase benchmark scores reported in the paper.

Recommended final wording for addressing the partial result:

> The pilot used ten frozen WebQSP questions. After an answer-independent degree cap, nine questions remained resource-eligible. Gold-SPARQL filtering retained six answerable questions. The local Qwen2.5 7B run produced two relaxed matches out of six evaluated questions. This result is small, but it is useful because it makes the infrastructure assumptions behind GoG visible.

## 2. Code Submission

Submit the GitHub repository:

https://github.com/KiiraV/Seminar-KG-and-LLM

The code submission should point to these files:

| Purpose | Path |
|---|---|
| Main project overview | `README.md` |
| Reimplementation entry point | `Reimplementation/README.md` |
| Formal pilot protocol | `Reimplementation/Formal Pilot Guide.md` |
| Lightweight formal-pilot code | `Reimplementation/formal_partial_experiment/` |
| Saved evidence display script | `Reimplementation/show_formal_result.sh` |
| Partial setup guide | `Reimplementation/Partial Setup Guide.md` |
| Code structure analysis | `Reimplementation/Code Structure Analysis.md` |
| Results summary | `Reimplementation/Results.md` |
| Reproduction audit | `Reimplementation/Reproduction Audit.md` |
| Experiment protocol | `Experiment/README.md` |
| Formal pilot result | `Experiment/Formal Partial Experiment.md` |
| Machine-readable evidence | `Experiment/Formal Pilot Evidence.json` |
| Demo evidence | `Experiment/DEMO Pipeline Evidence.json` |

Do not submit generated local databases, `.env` files, API keys, model weights, local virtual environments, or local absolute paths.

## 3. Verified Local Result

The local formal result script was run successfully on 31 July 2026.

Command used:

```bash
# from the local GoG demonstration checkout
cd GoG
./show_formal_result.sh
```

Verified output:

```text
Scope: small-scale formal partial-Freebase pilot
Data source: https://qlever.dev/api/freebase
frozen_questions: 10
resource_eligible_questions: 9
gold_sparql_answerable_questions: 6
model_entities: 4536
model_triples: 47523
bm25_names: 12640
model: qwen2.5:7b
runtime: Ollama in Docker
correct: 2
evaluated: 6
relaxed_answer_match: 0.333
```

This output can be used as evidence that the local reproduction pipeline is runnable.

## 4. GitHub Cleanliness Check

Before final push:

```bash
cd Seminar-KG-and-LLM
python3 tools/check_repository.py
git status --short
```

Current known issue from the repository checker:

- Several draft/support Markdown files contain local absolute paths.

Suggested final-push policy:

- Push stable documentation and experiment evidence.
- Do not push old draft support files that contain local paths.
- If keeping them, remove local paths first.
- Use `GitHub Submission Manifest 2026-07-31.md` as the final upload list.

## 5. What To Say If Asked About Reproduction

Short answer:

> I could not reproduce the full paper benchmark because full Freebase deployment was not feasible locally. Instead, I implemented a resource-constrained partial-Freebase pilot. I separated engineering validation from formal evaluation to avoid gold-triple leakage. The formal pilot freezes questions before graph construction, builds a partial graph independently from QLever Freebase, filters answerable questions afterward, and runs GoG with a local Qwen2.5 7B model.

Longer answer:

> The main result is not a competitive benchmark score but a verified reproduction workflow. The code demonstrates graph construction, Virtuoso/SPARQL querying, BM25 entity linking, GoG reasoning, prediction logging, and evaluation. The local result is 2/6 relaxed answer match on the retained answerable subset. I report it carefully because graph coverage, model scale, and sample size differ from the original paper.
