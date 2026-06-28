import os
import warnings
from dotenv import load_dotenv

# Import Gemini and LangChain components
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
import gradio as gr

# Load environment variables (API Key)
load_dotenv()

# Suppress warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn
warnings.filterwarnings('ignore')

## LLM Initialization
def get_llm():
    # Use Gemini model
    # Ensure GOOGLE_API_KEY is set in your .env file or environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.5,
    )
    return llm

## Embedding model
def get_embedding_model():
    # Use Google GenAI Embeddings
    api_key = os.getenv("GOOGLE_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    return embeddings

## Document loader
def document_loader(file_path):
    loader = PyPDFLoader(file_path)
    loaded_document = loader.load()
    return loaded_document

## Text splitter
def text_splitter(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = splitter.split_documents(data)
    return chunks

## Vector db
def vector_database(chunks):
    embedding_model = get_embedding_model()
    # Create vector database using Chroma
    vectordb = Chroma.from_documents(chunks, embedding_model)
    return vectordb

## Retriever
def retriever(file_path):
    splits = document_loader(file_path)
    chunks = text_splitter(splits)
    vectordb = vector_database(chunks)
    retriever_obj = vectordb.as_retriever()
    return retriever_obj

## QA Chain
def retriever_qa(file, query):
    if file is None:
        return "Please upload a PDF file first."
    
    # file object from Gradio has a 'name' attribute which is the path
    file_path = file.name if hasattr(file, 'name') else file
    
    llm = get_llm()
    retriever_obj = retriever(file_path)
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever_obj, 
        return_source_documents=False
    )
    response = qa.invoke(query)
    return response['result']

# Create Gradio interface
rag_application = gr.Interface(
    fn=retriever_qa,
    allow_flagging="never",
    inputs=[
        gr.File(label="Upload PDF File", file_count="single", file_types=['.pdf'], type="filepath"),
        gr.Textbox(label="Input Query", lines=2, placeholder="Type your question here...")
    ],
    outputs=gr.Textbox(label="Output"),
    title="Gemini RAG Chatbot",
    description="Upload a PDF document and ask any question. The chatbot will try to answer using the provided document and Google Gemini."
)

# Launch the app
if __name__ == "__main__":
    # Note: server_name="0.0.0.0" allows external access, share=True creates a public link
    rag_application.launch(server_name="0.0.0.0", server_port=7860, share=True)
