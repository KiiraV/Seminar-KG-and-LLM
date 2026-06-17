During the reimplementation, I found that the Freebase setup is the main bottleneck. The original repository assumes a local Virtuoso endpoint over Freebase, but the linked data source is no longer a straightforward downloadable benchmark package. Therefore, I updated the reimplementation plan to distinguish between two settings: full Freebase deployment and partial-KG deployment.

For the partial-KG setting, the evaluation protocol also needs to change: only questions whose answers are contained in the deployed KG should be retained.
