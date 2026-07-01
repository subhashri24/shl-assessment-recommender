from fastapi import FastAPI
from pydantic import BaseModel
from chat import chat
import os

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat_api(request: ChatRequest):

    messages = [m.model_dump() for m in request.messages]

    reply, recs, end = chat(messages)

    recommendations = []

    for r in recs:

        recommendations.append(
            {
                "name": r["name"],
                "url": r["url"],
                "test_type": r["test_type"]
            }
        )

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": end
    }