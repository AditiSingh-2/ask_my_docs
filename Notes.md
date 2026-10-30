\# Experiment Notes



\## Token usage (Gemini thinking model)

| Field | Run 1 | Meaning |

|---|---|---|

| prompt\_token\_count | 21 | Tokens sent (question + system prompt) |

| candidates\_token\_count | 61 | Tokens in the visible answer |

| thoughts\_token\_count | 630 | Tokens spent "thinking" before answering |

| total\_token\_count | 712 | 21 + 61 + 630 |



\- Thinking tokens count toward `max\_output\_tokens` and toward cost.

\- `max\_output\_tokens=200` cut the answer off mid-sentence; 500-1024 worked.

\- The limit applies to output only: thinking 450 + answer 39 = 489 (under 500).

&#x20; Total 507 includes 18 prompt tokens, which the limit doesn't count.



\## Step 1: prompt and temperature

\- Pirate system prompt: followed both instructions (18 prompt / 39 answer / 451 thinking).

\- Temperature 0.0, 3 runs: wording differed every time, so temp 0 is NOT fully deterministic.

\- Thinking tokens were stable across runs (451, 453, 450).



\## Retrieval findings

\- Retrieval always returns top-k, even when the answer isn't in the document.

\- An unanswerable question (India AR/VR company) scored 0.692, higher than an

&#x20; answerable one (0.676). A score threshold alone can't detect "not in document",

&#x20; so the LLM prompt has to handle refusal.

\- Chunk boundaries can split a heading from its content (chunk 23 ends "Hardwa").

\- Fixed-size chunking cuts words in half; sentence-based splitting is worth trying.



\## Eval results (10 questions: 8 answerable, 2 unanswerable)

\- Accuracy 10/10 with keyword grading.

\- Avg tokens per query: 385 prompt, 236 thinking, 25 answer.

\- Latency not reported: the run was inflated by free-tier rate-limit waits

&#x20; (5 requests/min). Single requests took about 4-6 s.

\- Limitations: keyword grading and a small test set.



\## Ideas not yet tried

\- Chunk size 800 vs 500, higher k

\- Temperature 1.0 vs 0.0 on the eval

\- Chroma/FAISS instead of numpy, LLM-as-judge grading

