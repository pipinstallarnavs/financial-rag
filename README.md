![Financial RAG banner](assets/banner.svg)

# Financial RAG

An auditable retrieval-augmented generation baseline for numerical questions over financial reports.

## Approach

The system indexes report sentences and table rows from FinQA, retrieves evidence for each question, and executes the dataset's arithmetic programs in a restricted interpreter. Retrieval is evaluated independently before answer generation, and answer fields never enter the index.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py --limit 300
python -m unittest -v
```

## Design goals

- Keep retrieved evidence visible
- Separate retrieval quality from arithmetic execution
- Restrict executable operations to a small audited vocabulary
- Make numerical answers reproducible from cited report fragments

## Scope

The project is a baseline over FinQA excerpts. It does not cover arbitrary filings, open-ended financial research, or production document ingestion.
