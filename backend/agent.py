from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.language_models import BaseChatModel
from models import ChartQuery, ChatResponse, Project, Task, Resource
from langchain.tools import Tool

from os import linesep

class Agent(object):
    __llm = BaseChatModel
    __executor: AgentExecutor
    __parser: PydanticOutputParser
    __prompt: ChatPromptTemplate

    def __init__(self, model_name: str, system: str, tools: list[Tool] = []) -> None:
        self.__llm = ChatOllama(model=model_name,temperature=0)
        self.__parser = PydanticOutputParser(pydantic_object=ChatResponse)
        # self.__parser = PydanticOutputParser(pydantic_object=model)
        system += linesep + "Wrap the output in this format use the 'answer' field for your response and reasoning, use the rest of the fields for data. Do no provide no other text"+linesep+"{format_instructions}"
        self.__prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("placeholder", "{chat_history}"),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        ).partial(format_instructions=self.__parser.get_format_instructions())

        agent = create_tool_calling_agent(llm=self.__llm, prompt=self.__prompt, tools=tools)
        self.__executor = AgentExecutor(agent=agent, tools=tools)

    def run(self, query: ChartQuery) -> ChatResponse | None:
        response = self.__executor.invoke(query.model_dump())
        try:
            return self.__parser.parse(response.get("output"))
        except Exception as e:
            print(f"Cannot parse response: {e}")
            return None
    
