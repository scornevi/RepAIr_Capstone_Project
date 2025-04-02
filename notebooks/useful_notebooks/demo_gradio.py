import gradio as gr
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import IFixitLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
import warnings

warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# API key setup
groq_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=groq_key)
llm = client

# Function to split documents
def split_documents(documents, chunk_size=800, chunk_overlap=80):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents=documents)

# Function to create FAISS vector database
def create_embedding_vector_db(chunks):
    embedding = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )
    return FAISS.from_documents(documents=chunks, embedding=embedding)

# Function to query vector database
def query_vector_db(query, vector_db):
    docs = vector_db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"Use the following context:\n{context}"},
            {"role": "user", "content": query},
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=True
    )
    for chunk in chat_completion:
        yield chunk.choices[0].delta.content

# Function to rewrite user query
def rewrite_query(user_input):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": """Rewrite the following user query into a structured format, 
             ensuring it includes the device type, model, and specific repair issue."""},
            {"role": "user", "content": user_input},
        ],
        model="llama3-8b-8192",
        temperature=0
    )
    return chat_completion.choices[0].message.content

# Load data only when necessary
data = None
def load_data():
    global data
    if data is None:
        data = IFixitLoader.load_suggestions("iPhone 6", doc_type='guide')

def chatbot_interface(history, user_query):
    if not user_query.strip():
        return history + [(user_query, "Please enter a valid query.")]
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Determine if the following user input requires technical repair assistance."},
            {"role": "user", "content": user_query},
        ],
        model="llama3-8b-8192",
        temperature=0
    )
    needs_repair_assistance = "yes" in chat_completion.choices[0].message.content.lower()
    
    if not needs_repair_assistance:
        return history + [(user_query, chat_completion.choices[0].message.content)]
    
    load_data()
    chunks = split_documents(data)
    vector_db = create_embedding_vector_db(chunks)
    
    optimized_query = rewrite_query(user_query)
    return history + [(user_query, query_vector_db(optimized_query, vector_db))]

def main():
    with gr.Blocks() as app:
        gr.Markdown("# 🔧 Fix it! LLaMA3-8B-8192 Chatbot")
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(placeholder="What would you like to repair?")
        submit_btn = gr.Button("Submit")
        
        submit_btn.click(chatbot_interface, [chatbot, user_input], chatbot)
        user_input.submit(chatbot_interface, [chatbot, user_input], chatbot)
    
    app.queue().launch()

if __name__ == "__main__":
    main()