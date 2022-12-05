from pydantic import BaseModel

class AnalyzersForm(BaseModel):
    ioc: str
    selected_analyzers: list[str]
    

