from langchain_community.vectorstores import SKLearnVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from typing import Iterable

class VectorStore(object):
    __embeddings: OllamaEmbeddings
    __db: Chroma

    def __init__(self, model_name: str = "mxbai-embed-large") -> None:
        self.__embeddings = OllamaEmbeddings(model=model_name)
        self.__db = Chroma(collection_name="project_data", embedding_function=self.__embeddings,persist_directory="./chroma/store")
            
    def add_item(self, json: str, id:str, item_type:str) -> None:
        doc = Document(page_content=json, metadata={"item_type": item_type})
        self.__db.add_documents(documents=[doc], ids=[id])
        
    def update_item(self, json: str, id:str, item_type:str) -> None:
        doc = Document(page_content=json, metadata={"item_type": item_type})
        self.__db.update_document(id, doc)
        
    def delete_item(self, id:str) -> None:
        self.__db.delete([id])
        
    def find_items(self, query: str, item_type: str|None = None) -> Iterable[tuple[str, str]]:
        docs = self.__db.similarity_search(query=query, k=1, filter={"item_type", item_type}) if item_type else self.__db.similarity_search(query=query, k=1)
        for doc in docs:
            yield doc.page_content, doc.metadata["item_type"]
    
    def addFiles(self, files: list[str]) -> None:
        for file in files:
            docs = self.load_file(file)
            self.__db.add_documents(docs)

    def add(self, text: str) -> None:
        self.__db.add_documents(Document(text))

    def load_file(self, file: str) -> list[Document]:
        doc = TextLoader(file).load()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
        docs_splits = text_splitter.split_documents(doc)
        return docs_splits
    
    def get(self, query: str) -> list[Document]:
        retriever = self.__db.as_retriever(k=4)
        return retriever.invoke(query) 
    
    def reset(self) -> None:
        self.__db.reset_collection()

def get_retriever(docs_split: list[Document], model_name: str = "llama3.2") -> VectorStoreRetriever:
    vector_store = SKLearnVectorStore.from_documents(documents=docs_split, embedding=OllamaEmbeddings(model=model_name))
    retriever = vector_store.as_retriever(k=4)
    return retriever