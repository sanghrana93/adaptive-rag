from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def handle_simple_query(query, openai_api_key):
    """
    Handle simple queries using a basic OpenAI completion.
    """
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
    response = llm(query)
    return response

def handle_complex_query(query, vector_store, openai_api_key):
    """
    Handle complex queries using Retrieval-Augmented Generation (RAG).
    """
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=openai_api_key, temperature=0.7),
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    response = qa.run(query)
    return response