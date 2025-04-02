from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import bs4

def get_docs_list() -> list[Document]:
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]

    docs = []
    for url in urls:
        loader = WebBaseLoader(url)
        doc = loader.load()
        docs.append(doc)
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)

    docs_splits = text_splitter.split_documents(docs_list)

    return docs_splits

def get_documents(files: list[str]) -> list[Document]:
    docs = []
    for file in files:
        doc = TextLoader(file).load()
        docs.append(doc)

    docs_list = [item for sublist in docs for item in sublist]
    
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)

    docs_splits = text_splitter.split_documents(docs_list)

    return docs_splits
