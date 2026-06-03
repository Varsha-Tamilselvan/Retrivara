from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

def create_rag_chain(vectorstore):
    
  llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.3
   )


  prompt = ChatPromptTemplate.from_template(
    """ Answer the question using only the context below.

        Context:
        {context}

        Question:
        {input}

        Answer:
    """
)



  document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt
)



  retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
   )



  retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
  )
  return retrieval_chain
