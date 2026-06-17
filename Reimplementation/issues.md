# Issue 1

## Freebase Dump Access and Resource Limitation

The original implementation assumes access to a full local Freebase deployment. During reimplementation, the original download instruction was found to be insufficient because the linked Freebase resource is a deprecated historical dump page rather than a complete runnable setup package.

The tutor clarified that Freebase must be deployed locally with Virtuoso. If full deployment is not possible, a partial dump may be used, but the benchmark must be filtered to questions answerable by that partial dump.

Impact:
- Full reproduction requires high storage and long import time.
- Partial reproduction changes the evaluation set.
- Reported results must clearly state whether they use full Freebase or a filtered partial KG.
