import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from retrieve import retrieve

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

GEN_MODEL = "gemini-3.7-flash"

SYSTEM_PROMPT = (
    "You answer questions using ONLY the context provided. "
    "If the context does not contain the answer, reply exactly: "
    "I don't know based on the provided document. "
    "Do not use outside knowledge."
)


def ask(question, k=3):
    start = time.time()
    results = retrieve(question, k)
    context = "\n\n---\n\n".join(chunk for _, _, chunk in results)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"

    response = None
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=GEN_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.0,
                    max_output_tokens=1024,
                ),
            )
            break
        except Exception as e:
            wait = 60 if "429" in str(e) else 10 * (attempt + 1)
            print(f"Attempt {attempt + 1} failed: {str(e)[:300]}")
            time.sleep(wait)

    if response is None:
        raise RuntimeError("Generation failed 5 times")

    usage = response.usage_metadata
    return {
        "answer": response.text,
        "sources": [
            {"chunk_id": i, "score": round(s, 3), "text": c}
            for i, s, c in results
        ],
        "latency_ms": round((time.time() - start) * 1000),
        "tokens": {
            "prompt": usage.prompt_token_count,
            "answer": usage.candidates_token_count,
            "thinking": usage.thoughts_token_count,
        },
    }


if __name__ == "__main__":
    question = input("Ask a question: ")
    result = ask(question)
    print("\nANSWER:", result["answer"])
    print("SOURCE CHUNKS:", [s["chunk_id"] for s in result["sources"]])
    print("LATENCY (ms):", result["latency_ms"])
    print("TOKENS:", result["tokens"])