from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool

def get_search_tool() -> Tool:
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="search",
        func=search.run,
        description="Search the web for information",
    )
    return search_tool

def get_wiki_tool() -> Tool:
    wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
    return WikipediaQueryRun(api_wrapper=wrapper)