from typing import Any
from abc import ABC,abstractmethod
class Client(ABC):
    def __init__(self,
                 name:str,
                 api_key:str,
                 base_url:str):
        self.name:str = name
        self.api_key:str = api_key
        self.base_url:str = base_url

    @abstractmethod
    def chat(self,config:Any):
        raise ImportError()
    @abstractmethod
    def async_chat(self,config:Any):
        raise ImportError()