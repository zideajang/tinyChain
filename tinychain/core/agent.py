from abc import ABC,abstractmethod
from tinychain.core.client import Client
class Agent:
    def __init__(
            self,
            name:str,
            client:Client
            
            ):
        self.name = name
        self.client = client

    @abstractmethod
    def async_run(self,query):
        pass