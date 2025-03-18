from typing import Protocol,List,Dict,Any,Union
from pydantic import BaseModel,Field
from .recursive_character_text_splitter import RecursiveCharacterTextSplitter

class Doc(BaseModel):
    content:str = Field(title="content")
    metadata:Dict[str,Any] = Field(title="metada",default_factory=dict)


class Splitter(Protocol):
    def split_text(self, text)->Union[List[str],List[Doc]]:
        ...


__all__ = (
    "RecursiveCharacterTextSplitter",
    "Doc",
    "Splitter"
)