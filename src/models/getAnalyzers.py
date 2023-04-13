from pydantic import BaseModel

class GetAnalyzers(BaseModel):
    type: str | None