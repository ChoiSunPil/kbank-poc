from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class KbankQueryState(TypedDict):
    query: str
    decision: str
    documents: list
    bank_name: str
    answer: str
