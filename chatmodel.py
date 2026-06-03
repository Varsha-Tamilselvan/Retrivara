from dotenv import load_dotenv
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from langchain_community.llms import HuggingFaceHub

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

# api_key = os.getenv("API_KEY")

# if not api_key:
#     raise ValueError("API_KEY not found in .env file")

# os.environ["HUGGINGFACEHUB_API_TOKEN"] = api_key

# --------------------------------------------------
# Step 1: Sample Document
# --------------------------------------------------

document = """
Reinforcement learning (RL) is a machine learning paradigm
where an agent learns by interacting with an environment.

The agent takes actions and receives rewards or penalties.
The goal is to maximize cumulative reward over time.

Applications include robotics, game playing, autonomous
vehicles, and recommendation systems.
"""

print("Document length:", len(document))

# --------------------------------------------------
# Step 2: Text Splitting
# --------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunks = splitter.split_text(document)

print("\nChunks created:", len(chunks))

# --------------------------------------------------
# Step 3: Embeddings
# --------------------------------------------------

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embeddings loaded successfully")

# --------------------------------------------------
# Step 4: Create Vector Store
# --------------------------------------------------

print("\nCreating Chroma DB...")

vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Vector DB created")

# --------------------------------------------------
# Step 5: Similarity Search
# --------------------------------------------------

query = "What is reinforcement learning?"

docs = vectorstore.similarity_search(
    query=query,
    k=3
)

print("\nRetrieved Documents:")

for i, doc in enumerate(docs, start=1):
    print(f"\nDocument {i}")
    print(doc.page_content)

# --------------------------------------------------
# Step 6: Load LLM
# --------------------------------------------------

print("\nLoading LLM...")

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.3
)

# --------------------------------------------------
# Step 7: Create Prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_template(
    """
Answer the question using only the context below.

Context:
{context}

Question:
{input}

Answer:
"""
)

# --------------------------------------------------
# Step 8: Create Document Chain
# --------------------------------------------------

document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt
)

# --------------------------------------------------
# Step 9: Create Retriever
# --------------------------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# --------------------------------------------------
# Step 10: Create Retrieval Chain
# --------------------------------------------------

retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)

# --------------------------------------------------
# Step 11: Ask Questions
# --------------------------------------------------

questions = [
    "What is reinforcement learning?",
    "How does an agent learn?",
    "Give some applications of reinforcement learning."
]

for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)

    response = retrieval_chain.invoke(
        {"input": question}
    )

    print("\nANSWER:")
    print(response["answer"])