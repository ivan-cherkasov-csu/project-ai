from langchain_core.language_models import BaseChatModel
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from pydantic import BaseModel
from os import linesep

class StructuredOutputAgent(object):
    __parser: PydanticOutputParser
    __executor: AgentExecutor

    def __init__(self, llm: BaseChatModel, system: str, model: BaseModel, tools: list[Tool] = []) -> None:
        self.__parser = PydanticOutputParser(pydantic_object=model)
        system += linesep + "Wrap the output in this format and provide no other text"+linesep+"{format_instructions}"
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("placeholder", "{chat_history}"),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        ).partial(format_instructions=self.__parser.get_format_instructions())
        self.__executor = AgentExecutor(create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools), tools=tools)
    
    def run(self, params: dict[str, str]) -> BaseModel | None:
        response = self.__executor.invoke(params)
        try:
            return self.__parser.parse(response.get("output")[0]["text"])
        except Exception as e: 
            print("Error parsing response: ", e)
            return None
        