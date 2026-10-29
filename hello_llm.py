import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # reads your .env file
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


for attempt in range(3):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents="Explain what RAG is.",
            config=types.GenerateContentConfig(
                system_instruction="You are a pirate. Answer in one sentence.",
                temperature=0.0,
                max_output_tokens=500,
            ),
        )
        print(response.text)
        print(response.usage_metadata)
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")

        time.sleep(3)
        