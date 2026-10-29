def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


if __name__ == "__main__":
    text = load_text("docs/sample.txt")
    chunks = chunk_text(text)

    print(f"Document length: {len(text)} characters")
    print(f"Number of chunks: {len(chunks)}")
    print("--- First chunk ---")
    print(chunks[0])
    print("--- Second chunk ---")
    print(chunks[1])