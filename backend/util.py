from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableSerializable
from langchain_core.language_models import BaseChatModel
from langchain.agents import create_tool_calling_agent, AgentExecutor

def create_agent(llm: BaseChatModel, prompt: PromptTemplate, tools: list[any] = []) -> AgentExecutor:
    agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
    exec = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return exec 

def init_model() -> ChatOllama:
    # llm = ChatOllama(model='llama3.2', temperature=0)
    llm = ChatOllama(model='qwen2.5',temperature=0)
    # llm = ChatOllama(model='deepseek-r1:7b',temperature=0)
    return llm
