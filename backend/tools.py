from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from storage import Storage

def get_search_tool() -> Tool:
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="web_search",
        func=search.run,
        description="Search the web for information",
    )
    return search_tool

def get_rag_tool(storage: Storage) -> Tool:
    local_search = Tool(
        name = "local_search",
        func = storage.run,
        description="Search local storage for existing Projects, Tasks, and Resources"
    )
    return local_search
    
def get_wiki_tool() -> Tool:
    wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
    return WikipediaQueryRun(api_wrapper=wrapper)