from typing import List

from coderag.logging import logger
from langchain_community.document_loaders.generic import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class CodeBaseStore:
    def __init__(self, model_name:str=None):
        self.db = None
        self._store:Chroma = Chroma(HuggingFaceEmbeddings(model_name=model_name))
        
    def store(self, documents:List[Document]):
        self.db = self._store.from_documents(documents)
        
    def embed():
        pass
    
    def store():
        pass
    
    def search():
        pass

