# Evaluation Plan

Create a JSONL dataset:

```json
{"question":"How many annual leave days do employees receive?","expected":"20"}
{"question":"How often can employees work remotely?","expected":"up to three days per week"}
```

For a serious portfolio version, add:

- retrieval precision@k
- retrieval recall@k
- answer relevance
- faithfulness / groundedness
- latency
- token usage
- cost per query

The evaluation runner should compare the retrieved context against expected evidence,
rather than only checking whether the final answer contains a keyword.
