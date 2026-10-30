import json
import time
from answer import ask

with open("eval/questions.json", encoding="utf-8") as f:
    questions = json.load(f)


def norm(text):
    return text.lower().replace("\u2019", "'")


def passed(item, answer):
    a = norm(answer)
    if item.get("refusal"):
        return "i don't know" in a
    ok = any(norm(w) in a for w in item["expect_any"])
    ok = ok and all(norm(w) in a for w in item.get("also", []))
    return ok


results = []
for item in questions:
    r = ask(item["q"])
    ok = passed(item, r["answer"])
    results.append((ok, r))
    print(f"{'PASS' if ok else 'FAIL'} | {r['latency_ms']} ms | {item['q']}")
    if not ok:
        print(f"   answer: {r['answer'][:200]}")
    time.sleep(15)  

n = len(results)
print(f"\nAccuracy: {sum(ok for ok, _ in results)}/{n}")
print(f"Avg latency: {sum(r['latency_ms'] for _, r in results) / n:.0f} ms")
print(f"Avg prompt tokens: {sum(r['tokens']['prompt'] for _, r in results) / n:.0f}")
print(f"Avg thinking tokens: {sum(r['tokens']['thinking'] for _, r in results) / n:.0f}")
print(f"Avg answer tokens: {sum(r['tokens']['answer'] for _, r in results) / n:.0f}")
