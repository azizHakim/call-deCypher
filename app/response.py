import os
import json
import threading
import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from dotenv import load_dotenv
from scraper import get_article_links, get_article_data

# Load environment variables
load_dotenv()

max_article_number =  int(os.getenv("MAX_ARTICLE_NUMBER"))

# Function to get lates news related to the prompt
def get_data(prompt):
    # Fetch article links related to the prompt
    article_links = get_article_links(prompt)
    article_list = []
    threads = []

    # Multithreaded fetching of article data
    for link in article_links:
        thread = threading.Thread(target=get_article_data, args=(link, article_list))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return article_list

# Initialize service context with OpenAI model
service_context = ServiceContext.from_defaults(
    llm=OpenAI(
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.5,
        system_prompt="You are an expert on financial analysis and your job is to answer questions about finances using the latest news. If a question is not about finance respond generally.",
    )
)


def load_default_data():
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    docs = reader.load_data()
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    return index

# Load default data into index
index = load_default_data()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.header("Chat with a virtual finance Guru")

# Initialize chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about latest financial news",
        }
    ]

# Initialize chat engine
chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)

# User input prompt
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking, great responses takes a few seconds...."):
            # Update the index based on user prompt
            article_list = get_data(prompt)
            docs = load_data(article_list)
            print("all docs", docs)
            index.refresh(docs)
            chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)

            # Generate response
            response = chat_engine.chat(prompt)

            # Display response
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history