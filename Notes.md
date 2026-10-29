Field	Value	Meaning(maX_token=1024)
prompt_token_count	21	Tokens you sent (your question plus the system prompt)
candidates_token_count	61	Tokens in the visible answer you read
thoughts_token_count	630	Tokens the model spent “thinking” before answering
total_token_count	712	All of it added up: 21 + 61 + 630 = 712

 max_token=500,temp=0.0,total=508

prompt_token_count
candidates_token_count
thoughts_token_count
# Step 1 experiments
- Pirate system prompt: followed both instructions. Tokens: 18 prompt / 39 answer / 451 thinking.
- Temperature 0.0, 3 runs: (what did you see?)
- Temperature 1.5, 3 runs: (what did you see?)
- max_output_tokens=20: (what happened?)
- Learned: thinking tokens count toward the output limit and cost.
- Temperature 0.0, 2 runs: wording was different both times, so temp 0 is NOT fully deterministic.
  Thinking tokens: 451 and 453 (stable).
#3
thinking 450 + answer 39 = 489 output tokens  (under 500, so it fit)
489 + 18 prompt tokens   = 507 total          (prompt isn't counted in the limit)