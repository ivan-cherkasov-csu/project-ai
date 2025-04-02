from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableSerializable
from langchain_core.language_models import BaseChatModel
from langchain.agents import create_tool_calling_agent, AgentExecutor
from os import linesep

def get_prompt_template() -> PromptTemplate:
    prompt = PromptTemplate(
        template="""You are an assistant for question-answering tasks.
        Use following documents to answer the question.
        If you don't know the answer, just say that you don't know.
        Use three sentences maximum and keep the answer concise:
        Question: {question}
        Documents: {documents}
        Answer:  
        """,
        input_variables=["question", "documents"]
    )
    return prompt

def create_agent(llm: BaseChatModel, prompt: PromptTemplate, tools: list[any] = []) -> AgentExecutor:
    agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
    exec = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return exec 

def init_model() -> ChatOllama:
    llm = ChatOllama(model='llama3.2', temperature=0)
    return llm

def get_rag() -> RunnableSerializable:
    rag_chain = get_prompt_template() | init_model() | StrOutputParser()
    return rag_chain

def call_and_parse(agent: AgentExecutor, params: dict[str, str], parser: PydanticOutputParser) :
    #params = {"query": "What is the capital of France?"}
    response = agent.invoke(params)
    try:
        structured_response = parser.parse(response.get("output")[0]["text"])
        return structured_response
    except Exception as e:
        print("Error parsing response", e)
        return None
