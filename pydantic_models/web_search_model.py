from pydantic import BaseModel, Field


class WebSearch(BaseModel):
    query: str = Field(description="question to search from web")
    limit: int = Field(description="the max number of web results you want to see",
                       default=3,
                       le=5)