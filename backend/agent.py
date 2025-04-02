from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel
from langchain.tools import Tool
from typing import TypeVar
from os import linesep

class Agent(object):
    __executor: AgentExecutor

    def __init__(self, llm: BaseChatModel, system: str, tools: list[Tool] = []) -> None:
        # self.__parser = PydanticOutputParser(pydantic_object=model)
        # system += linesep + "Wrap the output in this format and provide no other text"+linesep+"{format_instructions}"
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("placeholder", "{chat_history}"),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        )#.partial(format_instructions=self.__parser.get_format_instructions())
        self.__executor = AgentExecutor(agent=create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools), tools=tools)

    def run(self, params: dict[str, str]) -> str:
        answer = self.__executor.invoke(params).get("output")#["text"]
        return answer
    
