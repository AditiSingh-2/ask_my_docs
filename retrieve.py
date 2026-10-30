import numpy as np
from chunker import load_text, chunk_text
from embed import embed_texts

text = load_text("docs/sample.txt")
chunks = chunk_text(text)
vectors = np.load("vectors.npy")


def retrieve(question, k=3):
    q_vec = embed_texts([question], "RETRIEVAL_QUERY")[0]

    # cosine similarity between the question and every chunk
    scores = vectors @ q_vec / (
        np.linalg.norm(vectors, axis=1) * np.linalg.norm(q_vec)
    )

    top_ids = np.argsort(scores)[::-1][:k]
    return [(int(i), float(scores[i]), chunks[i]) for i in top_ids]


if __name__ == "__main__":
    question = input("Ask a question: ")
    for rank, (i, score, chunk) in enumerate(retrieve(question), start=1):
        print(f"\n#{rank} | chunk {i} | score {score:.3f}")
        print(chunk)