# %%
# pip install streamlit langchain openai faiss-cpu python-dotenv

# %%
import os
import streamlit as st
from langchain.document_loaders import IFixitLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# %%
# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit UI
st.title("🔧 iFixit Repair Assistant Chatbot")
st.write("Ask me about repair issues for your device!")

# User inputs device name
device_name = st.text_input("Enter your device (e.g., iPhone 6, MacBook Pro):")

# Load iFixit Data
if device_name:
    device_url = f"https://www.ifixit.com/Device/{device_name.replace(' ', '_')}" # issue must be fixed
    
    with st.spinner("Fetching repair guides..."):
        try:
            loader = IFixitLoader(device_url)
            device_data = loader.load()

            # Split and store documents
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.split_documents(device_data)

            vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())
            retriever = vectorstore.as_retriever()

            llm = ChatOpenAI(model="gpt-4")
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

            st.success(f"Loaded repair guides for {device_name} ✅")

            # Chatbot Input
            user_query = st.text_input("Ask a repair question:")

            if user_query:
                with st.spinner("Searching for answers..."):
                    response = qa_chain.run(user_query)
                    st.write("**Answer:**", response)

        except Exception as e:
            st.error("Could not load data. Make sure the device name is correct!")
            st.write(f"Error: {e}")

# querries dont work yet :-(   
# To run in this script in your shell terminal and initiate a streamlit browser app, 
# type this into shell:

# streamlit run .\notebooks\useful_notebooks\03_streamlit_API_LLama.py


