from langgraph.graph import StateGraph, START, END
from graph.KbankQueryState import KbankQueryState
from infra.datasource.vector.KbankWebVectorIndexer import KbankWebVectorIndexer
import yaml
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain import hub as prompts


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

    print(result)
    return result['answer']


@tool
def route_decision(decision: str) -> str:
    """질문을 분석하여 'vectordb', 'ml', 'llm' 중 하나를 결정합니다."""
    if decision not in {"vectordb", "ml", "llm"}:
        return "default"

    return decision


def make_decision(state: KbankQueryState) -> str:
    
    chain = prompts.pull("make_decision_prompt", include_model=True)

    response = chain.invoke({"query": state['query']})


    print(response.tool_calls)
    decision = response.tool_calls[0]['args']['decision']

    return decision


def query_by_vectordb(state: KbankQueryState):
    indexer = KbankWebVectorIndexer()
    documents = indexer.search(state.get("query"), 3)

    return {"decision": "vectordb", "documents": documents}


def query_by_llm(state: KbankQueryState):
    return {"decision": "llm"}


def query_by_ml(state: KbankQueryState):

    bank_name = "케이뱅크"

    return {"decision": "ml", "bank_name": bank_name}


def make_answer(state: KbankQueryState):
    
    chain = prompts.pull("answer_prompt", include_model=True)
    
    if state['decision'] == 'vectordb':
        context = "\n\n".join([doc.page_content for doc in state['documents']])
    else:
        context = None
        
    return {"answer": chain.invoke({"documents":context
                                    ,"query":state.get('query', '')
                                    ,"bank_name" : state.get('bank_name', '')
                                    }).content}
    
    
def load_answer_prompt() -> ChatPromptTemplate:
    base_dir = Path(__file__).resolve().parent.parent
    # yaml 경로 설정 (상대 경로로 접근)
    prompt_path = base_dir/ "infra" / "datasource" / "llm" / "prompt" / "answer_prompt.yaml"
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_dict = yaml.safe_load(f)
    return ChatPromptTemplate.from_template(prompt_dict["prompt_template"]["template"])


def load_make_decision_prompt() -> ChatPromptTemplate:
    base_dir = Path(__file__).resolve().parent.parent
    prompt_path = base_dir / "infra" / "datasource" / "llm" / "prompt" / "make_decision_prompt.yaml"
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_dict = yaml.safe_load(f)
    return ChatPromptTemplate.from_template(prompt_dict["prompt_template"]["template"])