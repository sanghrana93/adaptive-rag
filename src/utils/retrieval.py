import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS

def initialize_vector_store(file_path, openai_api_key):
    """
    Initialize a FAISS vector store from a PDF file.
    """
    print(f"Loading file from: {file_path}")  # Debug statement

    # Load the PDF file
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages from the PDF")  # Debug statement

    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_documents(texts, embeddings)

    return vector_store