from fastapi import APIRouter
from dto.QueryRequest import QueryRequest
from dto.QueryResponse import QueryResponse
from service.langraph_service import run_langraph_pipeline

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_langraph(request: QueryRequest):
    answer = run_langraph_pipeline(request.query)
    return QueryResponse(answer=answer)
