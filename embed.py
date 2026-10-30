import os
import time
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from chunker import load_text, chunk_text

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

EMBED_MODEL = "gemini-embedding-2"


def embed_texts(texts, task_type):
    for attempt in range(5):
        try:
            response = client.models.embed_content(
                model=EMBED_MODEL,
                contents=texts,
                config=types.EmbedContentConfig(task_type=task_type),
            )
            return np.array([e.values for e in response.embeddings])
        except Exception as e:
            wait = 60 if "429" in str(e) else 10 * (attempt + 1)
            print(f"Attempt {attempt + 1} failed: {str(e)[:300]}")
            time.sleep(wait)
    raise RuntimeError("Embedding failed 5 times")


if __name__ == "__main__":
    text = load_text("docs/sample.txt")
    chunks = chunk_text(text)

    vectors = embed_texts(chunks, "RETRIEVAL_DOCUMENT")

    print(f"Chunks: {len(chunks)}")
    print(f"Vector shape: {vectors.shape}")
    print(f"First 5 numbers of chunk 1: {vectors[0][:5]}")

    np.save("vectors.npy", vectors)
    print("Saved vectors.npy")