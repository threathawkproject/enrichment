from pydantic import BaseModel

class AnalyzersForm(BaseModel):
    ioc: str
    type: str
    selected_analyzers: list[str]   

