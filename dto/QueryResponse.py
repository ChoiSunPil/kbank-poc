from pydantic import BaseModel


class QueryResponse(BaseModel):
    answer: str