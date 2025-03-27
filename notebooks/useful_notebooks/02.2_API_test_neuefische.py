# %%
# General
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import IFixitLoader
# Langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub
from langchain.prompts.prompt import PromptTemplate
import streamlit as st

# two similar but different methods
from groq import Groq # direct groq call

import warnings
warnings.filterwarnings("ignore")

#%%
load_dotenv()

# %%
# credentials API key
groq_key = os.getenv('GROQ_API_KEY')
# USER_AGENT = os.getenv("USER_AGENT")

# for this test
client = Groq(api_key=groq_key)
llm = client # we use this as llm here

# %%
# retrieve data
data = IFixitLoader.load_suggestions("iPhone 6", doc_type = 'guide')

#%%
# functions
def split_documents(documents, chunk_size=800, chunk_overlap=80): # check chunk size and overlap for our purpose
    """
    this function splits documents into chunks of given size and overlap
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents=documents)
    return chunks

def create_embedding_vector_db(chunks #, db_name, target_directory=f"../vector_databases"
                               ):
    """
    this function uses the open-source embedding model HuggingFaceEmbeddings 
    to create embeddings and store those in a vector database called FAISS, 
    which allows for efficient similarity search
    """
    # instantiate embedding model
    embedding = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2' # EMBEDDING MODEL! converts text to vector ( stick to it)
    )
    # create the vector store 
    vector_db = FAISS.from_documents( # stores embeddings # from_documents includes metadata
        documents=chunks,
        embedding=embedding
    )
    return vector_db # will it work wihtout saving?

# Function to query the vector database and interact with Groq
def query_vector_db(query, vector_db):
    # Retrieve relevant documents
    docs = vector_db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # Interact with Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"Use the following context:\n{context}"},
            {"role": "user", "content": query},
        ],
        model="llama3-8b-8192",
        temperature=0 # optional: check best value!
    )
    return chat_completion.choices[0].message.content

#%%
# Streamlit app
st.title("Fix it! llama3-8b-8192")

# Extract text
text = data

# Chunk text
chunks = split_documents(text)
st.write("Cool! Text Chunked Successfully!")

# Generate embeddings and store in FAISS
vector_db = create_embedding_vector_db(chunks )
st.write("Cool! Embeddings Generated successfully!")

# User query input
user_query = st.text_input("What would you like to repair?")
if user_query:
    response = query_vector_db(user_query, vector_db)
    st.write("Response from LLM:")
    st.write(response)

