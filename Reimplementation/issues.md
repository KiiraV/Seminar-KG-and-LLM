## Full Freebase Deployment Limitation

The main reimplementation bottleneck is the Freebase setup. The original implementation requires a local Virtuoso deployment over the full Freebase dump. According to Google Freebase Data Dumps, the full Freebase triples contain approximately 1.9 billion triples, about 22 GB compressed and 250 GB uncompressed.

Due to storage and computation limitations, I cannot deploy the complete Freebase dump locally. Therefore, I follow the partial-dump strategy suggested by the tutor: deploy a partial Freebase dump through Virtuoso and filter the benchmark to retain only questions answerable by this partial KG.

This changes the evaluation setting. The results should be interpreted as partial-KG reimplementation results, not as a direct reproduction of the original full-Freebase results.
