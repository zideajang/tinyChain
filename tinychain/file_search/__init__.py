from typing import Protocol
from contextlib import contextmanager
from tinychain.utils import is_valid_csv_path

class Provider[T](Protocol):
    def get_data(self):
        ...
    def update_data(self):
        ...
    def delete_data(self):
        ...
    def save_data(self):
        ...

class CSVProvider:
    def __init__(self,file_path):
        self.file_path = file_path

class PlainTextProvider:
    def __init__(self,file_path):
        self.file_path = file_path
        with open(file_path,'r',encoding='utf-8') as f:
            self.content = f.read()

class SqliteProvider:
    def __init__(self,file_path):
        pass

@contextmanager
def resource(resource_path:str,resource_type:str=None):
     if resource_type:
         if resource_type == "sqlite":
             yield SqliteProvider(resource)
             
     if is_valid_csv_path(resource_path):
         yield CSVProvider(resource_path)