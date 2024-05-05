import os
import sys
from langchain import hub
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain_chroma import Chroma

from app import app
from app.process import process_result, post_process_facts
load_dotenv()

llm = ChatOpenAI(model="gpt-4",api_key=os.getenv("OPENAI_API_KEY"))


def get_facts(n_files, question, urls, api = False):
    loader = WebBaseLoader(urls)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": n_files})
    
    facts_prompt = ChatPromptTemplate.from_template("""
    The context is transcripts of one or more call logs. Your task is to answer the question according to the context. 
    The question will mostly ask you to deduce some facts discussed on the conversation.
    The answer to the questin can change over time in the conversation. 
    Give only the facts the persons finally decided to go forward with at the end of the conversation. 
    Give only the facts in a simple and clear language, use bulated list if there are multiple facts.
    Context: {context} 
    Question: {question} 
    Answer:"""                          
    )
    # exclude_prompt = PromptTemplate.from_template("""
    #                                               Given a list of facts return facts that are not active anymore
    #                                               Facts: {facts}
    #                                               Facts_final: """)
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    facts_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | facts_prompt
        | llm
        | StrOutputParser()
    )
    refine_facts_prompt = ChatPromptTemplate.from_template("""
        Given a list of facts remove unnecessary facts from the list. Return the remaining facts as it is in a bulated list.
        Facts: {facts}
        Necessary facts:"""
    )
    
    refine_facts_chain = ({"facts": facts_chain} | refine_facts_prompt | llm | StrOutputParser())

    response = refine_facts_chain.invoke(question)
    print(response)
    # post process response
    facts = post_process_facts(response)

    #store result
    if api == True:
        process_result(question, facts, app.config["RESULT_PATH"])

    else:
        return facts
