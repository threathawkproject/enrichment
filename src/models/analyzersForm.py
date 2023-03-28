from pydantic import BaseModel


class AnalyzersForm(BaseModel):
    ioc: str
    type: str
    selected_analyzers: list[str]


class FileSchema(BaseModel):
    file_name: str
    content_type: str
    contents: bytes
