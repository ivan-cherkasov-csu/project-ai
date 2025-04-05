from agent import Agent
from tools import get_rag_tool, get_search_tool, Storage
from os import system
from models import ChartQuery, ChatResponse

if __name__ == "__main__":
    system("cls")
    chat_agent_context = """You are an assistant for project management tasks.
        You can use tools and attached items if any to answer.
        If you don't know the answer, just say that you don't know."""
    
    query = 'Hey can you please find in local storage a project with the Chicken recipe?'   
    chat_agent = Agent(model_name='qwen2.5', system=chat_agent_context, tools=[get_search_tool(), get_rag_tool(Storage())])
    result = chat_agent.run(ChartQuery(query=query))
    print("Question:", query)
    print(result.answer)
    print("--------------------MODEL_START--------------------")
    print(result.model_dump_json())
    print("--------------------MODEL_END--------------------")
    query = "Please fix Chicken project from storage by adding relevant data, create task for each step in recipe, and add required resources. You can use web search to get data from the internet if you need."
    result = chat_agent.run(ChartQuery(query=query))
    print(result.answer)
    print("--------------------MODEL_START--------------------")
    print(result.model_dump_json())
    print("--------------------MODEL_END----------------------")