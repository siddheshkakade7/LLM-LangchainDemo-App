# LangGraph agent: builds graph with retrieval + LLM

from typing import List, TypedDict

from langgraph.graph import StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from app.config import Config
from app.retriever import get_retriever


class AgentState(TypedDict):
    question: str
    messages: List[BaseMessage]

Config.validate()

def add_user_message(state):
    state["messages"].append(HumanMessage(content=state["question"]))
    return state

def retrieve_context(state):
    retriever = get_retriever()
    docs = retriever.get_relevant_documents(state["question"])
    context = "\n\n".join([doc.page_content for doc in docs])
    state["messages"].append(HumanMessage(content=f"Context:\n{context}"))
    return state

def call_llm(state):
    llm = ChatOpenAI(
        api_key=Config.OPENAI_API_KEY,
        model=Config.MODEL_NAME,
        temperature=Config.TEMPERATURE
    )
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return state

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("user_input", RunnableLambda(add_user_message))
    graph.add_node("retrieve", RunnableLambda(retrieve_context))
    graph.add_node("llm", RunnableLambda(call_llm))

    graph.set_entry_point("user_input")
    graph.add_edge("user_input", "retrieve")
    graph.add_edge("retrieve", "llm")

    return graph.compile()
