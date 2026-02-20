## 2026-02-20 - [Quadratic Disk I/O Bottleneck in Vector Store Ingestion]
**Learning:** The `FaissVectorStore` implementation was rewriting the entire index to disk after *every* batch insertion. For large datasets, this transforms disk I/O from O(N) to O(N²), causing massive slowdowns as the index grows.
**Action:** Always verify if `save()` or `persist()` operations are incremental or full-rewrite. If full-rewrite, ensure they are called only once at the end of ingestion or at significant checkpoints, not per-batch.
