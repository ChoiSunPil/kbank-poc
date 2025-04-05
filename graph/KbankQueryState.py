from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class KbankQueryState(TypedDict):
    query: str
    documents: list
    answer: str