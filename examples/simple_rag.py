import ollama
from typing import Callable,Union,Optional,Dict,Any,List
from functools import wraps
from tinychain.core import Client
from tinychain.client.ollama_client import OllamaClient
from pydantic import BaseModel,Field
from tinychain.text_splitters import RecursiveCharacterTextSplitter,Doc,Splitter
from rich.console import Console
from tinychain.vector_store import ChromaStore,VectorStore
console = Console()
splitter = RecursiveCharacterTextSplitter(chunk_size=50,chunk_overlap=5,
                                          separators= ["\n\n", "\n", " ", "","。","，"])

from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434/api/embeddings",
)
client = OllamaClient(name="demo")
def ollama_embedding_fn(chunk):
    response = ollama.embeddings(model="nomic-embed-text:latest", prompt=chunk)
    embedding = response["embedding"]
    return embedding
store = ChromaStore(
    "simple_store",
    embedding_fn=ollama_embedding_fn
)

def rag(
        name:str,
        client:Client,
        model_name:str,
        store:VectorStore = None,
        splitter:Splitter = None,
        **api_params):

    def decorator(func:Callable):
        @wraps(func)
        def wrapper(*args,**kwargs):
            result,query = func(*args,**kwargs)
            console.print(f"query\n{query}")
            # TODO
            if isinstance(result,str):

                docs = []
                for idx, text in enumerate(splitter.split_text(result)):
                    docs.append(Doc(content=text,metadata={
                        "id":f"id_{idx+1}"
                    }))
                store.add_texts(
                    texts=[ doc.content for doc in docs],
                    metadatas=[doc.metadata for doc in docs ],
                    ids=[f"idx_{idx}" for idx in range(len(docs))]
                    )
                query_result = store.query([query])
                context = "<context>"
                for ctx in query_result['documents'][0]:
                    context += ctx
                context += "</context>"
                console.print(context)
                reseponse =  client.chat(
                    {
                        "model":model_name,
                        "messages":[
                            {'role':'system','content':context},
                            {'role': 'user', 'content': query}],
                        "stream":False
                        }
                        )
                
                return reseponse,query_result,docs
                
            return result
        return wrapper
    return decorator

@rag(name="simple_rag",client=client,model_name="qwen2.5",store=store,splitter=splitter)
def chat_with_doc(file_path,query):

    with open(file_path,"r",encoding='utf-8') as f:
        content = f.read()
    # process
    return content,query


if __name__ == "__main__":
    reseponse,query_result,docs = chat_with_doc("./data/blog.txt","结构化输出")
    console.print("切分结构",justify="center",style="green bold")
    for doc in docs:
        console.print(doc.content)

    console.print("检索结果",justify="center",style="green bold")
    print(query_result)
    console.print("询问结构",justify="center",style="green bold")
    print(reseponse.message.content)
    # for doc in docs:
    #     console.print(doc.content)
    #     console.print(len(doc.content))