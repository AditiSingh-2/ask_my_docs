from fastapi import FastAPI
from pydantic import BaseModel
from answer import ask

app = FastAPI(title="Ask My Docs")


class Question(BaseModel):
    question: str
    k: int = 3


@app.post("/ask")
def ask_endpoint(body: Question):
    return ask(body.question, body.k)