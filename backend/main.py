from util import get_rag, init_model
from vector_store import get_retriever
from splitter import get_docs_list
from agent import Agent

if __name__ == "__main__":
    # docs = get_docs_list()
    # retriever = get_retriever(docs)
    # chain = get_rag()
    
    # agent = Agent(retriever, chain)

    # question = "What is prompt engineering?"
    
    chat_agent_context = """You are an assistant for question-answering tasks.
        Use following documents to answer the question.
        If you don't know the answer, just say that you don't know.
        Use three sentences maximum and keep the answer concise:"""
     
    query = 'What is the capital of the France?'   
    chat_agent = Agent(llm=init_model(), system=chat_agent_context)
    answer = chat_agent.run({"query":query})
    print("Question:", query)
    print("Answer:", answer)