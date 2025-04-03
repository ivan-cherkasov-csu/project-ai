from agent import Agent
from tools import get_rag_tool, get_search_tool, Storage
from os import system
from models import ChartQuery, ChatResponse

if __name__ == "__main__":
    # docs = get_docs_list()
    # retriever = get_retriever(docs)
    # chain = get_rag()
    
    # agent = Agent(retriever, chain)

    # question = "What is prompt engineering?"
    system("cls")
    chat_agent_context = """You are an assistant for project management tasks.
        You can use tools and attached items if any to answer.
        If you don't know the answer, just say that you don't know."""
    
    query = 'Hey can you please find in local storage a project with "Honey Garlic Chicken" recipe?'   
    chat_agent = Agent(model_name='qwen2.5', system=chat_agent_context, tools=[get_search_tool(), get_rag_tool(Storage())])
    response = chat_agent.run(ChartQuery(query=query))
    print("Question:", query)
    print(response.answer)
    query = "Please add more relevant data to project details, create task for each step in recipe. You can use web search to get data from the internet if you need."
    response = chat_agent.run(ChartQuery(query=query))
    print(response.answer)
    print(response.model_dump_json())
    