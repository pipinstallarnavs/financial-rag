# Financial report RAG with cited arithmetic

Retrieve report sentences and table rows from FinQA, then run the dataset's
small arithmetic programs in a restricted interpreter. Retrieval is evaluated
before answer generation; answer/program fields never enter the index.

```bash
../NAS/venv/bin/python run.py --limit 300
../NAS/venv/bin/python -m unittest -v
```

This is an auditable numerical QA baseline over report excerpts, not a claim to
cover arbitrary filings or replace a financial analyst.
