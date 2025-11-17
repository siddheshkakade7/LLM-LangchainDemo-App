# FastAPI server exposing /chat endpoint

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import build_graph

app = FastAPI(title="LangGraph RAG Demo")
graph = build_graph()


@app.get("/")
def root():
    return {"status": "ok"}

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        state = {"question": req.question, "messages": []}
        result = graph.invoke(state)
        last_msg = result["messages"][-1]
        return ChatResponse(answer=last_msg.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
