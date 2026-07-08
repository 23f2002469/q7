import re
import time
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


MODEL_NAME = "task7-local"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str | None = MODEL_NAME
    messages: list[Message]
    stream: bool | None = False


def answer_prompt(prompt: str) -> str:
    token_match = re.search(r"\bTK[A-Za-z0-9]{6}\b", prompt)
    if token_match:
        return token_match.group(0)

    arithmetic_match = re.search(
        r"what\s+is\s+(\d{1,3})\s*\+\s*(\d{1,3})\??",
        prompt,
        flags=re.IGNORECASE,
    )
    if arithmetic_match:
        left = int(arithmetic_match.group(1))
        right = int(arithmetic_match.group(2))
        return str(left + right)

    return "I can help with echo and arithmetic prompts."


@app.post("/v1/chat/completions")
def chat_completions(payload: ChatRequest):
    prompt = payload.messages[-1].content if payload.messages else ""
    content = answer_prompt(prompt)

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": payload.model or MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }


@app.get("/")
def root():
    return {"ok": True, "endpoint": "/v1/chat/completions", "model": MODEL_NAME}
