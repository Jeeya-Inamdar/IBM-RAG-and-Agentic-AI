import os
import wget
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env
load_dotenv()

def setup_rag():
    # 1. Download the document
    filename = 'companyPolicies.txt'
    url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/6JDbUb_L3egv_eOkouY71A.txt'
    
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        wget.download(url, out=filename)
        print('\nFile downloaded')
    else:
        print(f"{filename} already exists.")

    # 2. Load and split the document
    loader = TextLoader(filename)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    print(f"Split document into {len(texts)} chunks")

    # 3. Embedding and storing
    print("Initializing embeddings and vector store...")
    embeddings = HuggingFaceEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)
    print('Document ingested into Chroma DB')

    # 4. Initialize Google Gemini LLM
    print("Initializing Gemini LLM...")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

    # 5. Setup Memory and Chain
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=docsearch.as_retriever(),
        memory=memory,
        get_chat_history=lambda h: h,
        return_source_documents=False
    )
    
    return qa_chain

def run_agent(qa_chain):
    history = []
    print("\n--- RAG Agent Ready! ---")
    print("You can ask questions about the company policies. Type 'quit', 'exit', or 'bye' to stop.\n")
    
    while True:
        query = input("Question: ")
        
        if query.lower() in ["quit", "exit", "bye"]:
            print("Answer: Goodbye!")
            break
            
        try:
            result = qa_chain.invoke({"question": query})
            answer = result["answer"]
            print(f"Answer: {answer}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        rag_chain = setup_rag()
        run_agent(rag_chain)
    except Exception as e:
        print(f"Critical Error during setup: {e}")
