\# Ask My Docs: RAG Q\&A API



A small retrieval-augmented generation (RAG) service built from scratch in Python.

Ask a question about a document and get an answer grounded in that document,

with the source chunks, latency and token usage returned.



\## How it works

1\. \*\*Chunk\*\* the document (500 characters, 50 overlap)

2\. \*\*Embed\*\* each chunk with a Gemini embedding model (3072-dim vectors)

3\. \*\*Retrieve\*\* the top-k chunks for a question using cosine similarity (NumPy)

4\. \*\*Generate\*\* an answer with a Gemini Flash model, told to answer ONLY from the retrieved context

&#x20;  and to say "I don't know" otherwise

5\. \*\*Serve\*\* it through FastAPI (`POST /ask`)



\## Stack

Python, FastAPI, NumPy, Gemini API (google-genai), python-dotenv, Git



\## Project structure

\- `chunker.py`: load and split text

\- `embed.py`: embed chunks and save `vectors.npy`

\- `retrieve.py`: cosine-similarity search

\- `answer.py`: prompt + LLM call, returns answer, sources, latency, tokens

\- `main.py`: FastAPI app

\- `run\_eval.py` + `eval/questions.json`: evaluation

\- `Notes.md`: experiment notes



\## Run it

```bash

python -m venv venv

venv\\Scripts\\activate          # Mac/Linux: source venv/bin/activate

pip install google-genai python-dotenv numpy fastapi uvicorn

```

Create a `.env` file with `GEMINI\_API\_KEY=your\_key`, then:

```bash

python embed.py                # builds vectors.npy (not stored in the repo)

uvicorn main:app --reload      # open http://127.0.0.1:8000/docs

```

Model names change often. Set `GEN\_MODEL` in `answer.py` and `EMBED\_MODEL` in `embed.py`

to models available to your key (list them with `client.models.list()`).



\## Evaluation

10 hand-written questions (8 answerable, 2 unanswerable), graded by keyword matching.

\- \*\*Accuracy: 10/10\*\*

\- Avg tokens per query: 385 prompt, 236 thinking, 25 answer

\- Latency is not reported: the full run was inflated by free-tier rate limits (5 requests/min).

&#x20; Single requests took about 4-6 s.

\- Limitations: small test set and keyword grading (can give false passes/fails).



\## Findings

\- Retrieval always returns top-k, even when the document has no answer. An unanswerable

&#x20; question scored 0.692, higher than an answerable one (0.676), so a similarity threshold

&#x20; can't detect "not in document". Refusal has to be handled in the prompt.

\- Thinking tokens count toward `max\_output\_tokens` and cost, and were larger than the visible answer.

\- Fixed-size chunking can cut words and split headings from their content.

\- Free-tier rate limits (429) and overloads (503) required retries with backoff.



\## Next steps

Chroma/FAISS instead of NumPy, chunk-size and k experiments, LLM-as-judge grading, Docker.



\## Data

Sample document: Wikipedia, "Augmented reality" (CC BY-SA).

