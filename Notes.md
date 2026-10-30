Field	Value	Meaning(maX\_token=1024)
prompt\_token\_count	21	Tokens you sent (your question plus the system prompt)
candidates\_token\_count	61	Tokens in the visible answer you read
thoughts\_token\_count	630	Tokens the model spent “thinking” before answering
total\_token\_count	712	All of it added up: 21 + 61 + 630 = 712

max\_token=500,temp=0.0,total=508

prompt\_token\_count
candidates\_token\_count
thoughts\_token\_count

# Step 1 experiments

* Pirate system prompt: followed both instructions. Tokens: 18 prompt / 39 answer / 451 thinking.
* Temperature 0.0, 3 runs: (what did you see?)
* Temperature 1.5, 3 runs: (what did you see?)
* max\_output\_tokens=20: (what happened?)
* Learned: thinking tokens count toward the output limit and cost.
* Temperature 0.0, 2 runs: wording was different both times, so temp 0 is NOT fully deterministic.
Thinking tokens: 451 and 453 (stable).
#3
thinking 450 + answer 39 = 489 output tokens  (under 500, so it fit)
489 + 18 prompt tokens   = 507 total          (prompt isn't counted in the limit)





\- Retrieval always returns top-k, even when the answer isn't in the doc.

\- Unanswerable question (India company) scored 0.692, higher than an answerable one (0.676).

&#x20; Score threshold alone can't detect "not in document". The LLM prompt must handle it.

\- Chunk boundaries can split a heading from its content (chunk 23 ends "Hardwa").

