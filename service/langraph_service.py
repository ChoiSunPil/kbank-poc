from langgraph.graph import StateGraph, START, END
from graph.KbankQueryState import KbankQueryState
from infra.datasource.vector.KbankWebVectorIndexer import KbankWebVectorIndexer
import yaml
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

def run_langraph_pipeline(query: str):
    workflow = StateGraph(KbankQueryState)

    ## node 추가
    workflow.add_node("query_by_vectordb", query_by_vectordb)
    workflow.add_node("query_by_ml", query_by_ml)
    workflow.add_node("query_by_llm", query_by_llm)
    workflow.add_node("make_answer", make_answer)

    # edge 추가
    workflow.add_conditional_edges(
        START,
        make_decision,
        {
            "vectordb": "query_by_vectordb",
            "ml": "query_by_ml",
            "llm": "query_by_llm",
            "default": END
        }
    )
    workflow.add_edge("query_by_vectordb", "make_answer")
    workflow.add_edge("query_by_ml", "make_answer")
    workflow.add_edge("query_by_llm", "make_answer")

    workflow.add_edge("make_answer", END)

    app = workflow.compile()
    result = app.invoke({"query": query})

    return result['answer']


def make_decision(state: KbankQueryState) -> str:
    return "vectordb"


def query_by_vectordb(state: KbankQueryState):
    indexer = KbankWebVectorIndexer()
    documents = indexer.search(state.get("query"), 3)
    return {"query": state['query'], "documents": documents}


def query_by_llm(state: KbankQueryState):
    return None


def query_by_ml(state: KbankQueryState):
    return None


def make_answer(state: KbankQueryState):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    answer_prompt = load_answer_prompt()
    context = "\n\n".join([doc.page_content for doc in state['documents']])
    messages = answer_prompt.format_messages(documents=context, query=state['query'])
    return {"query": state['query'], "documents": state['documents'], "answer": llm.invoke(messages).content}


def load_answer_prompt() -> ChatPromptTemplate:
    base_dir = Path(__file__).resolve().parent.parent
    # yaml 경로 설정 (상대 경로로 접근)
    prompt_path = base_dir/ "infra" / "datasource" / "llm" / "prompt" / "answer_prompt.yaml"
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_dict = yaml.safe_load(f)
    return ChatPromptTemplate.from_template(prompt_dict["prompt_template"]["template"])

