# vectorization functions
#%%
# General
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

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
    return vector_db # optimize

#Function to query the vector database and interact with Groq
def query_vector_db(query, vector_db):
    # Retrieve relevant documents
    docs = vector_db.similarity_search(query, k=3) # neigbors k are the chunks # similarity_search: FAISS function
    context = "\n".join([doc.page_content for doc in docs])

    # Interact with Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": f"Use the following context:\n{context}"},
            {"role": "user", "content": query},
        ],
        model="llama3-8b-8192",
        temperature=0 # optional: check best value!
    )
    return chat_completion.choices[0].message.content

def rewrite_query(user_input):
    """
    Uses the LLM to transform user input into a structured query for better iFixit searches.
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": """Rewrite the following user query into a structured format, 
             ensuring it includes the device type, model, and specific repair issue. 
             Return greetings when appropriate and ask questions to get information on 
             type, model, and specific repair issue from user."""},
            {"role": "user", "content": user_input},
        ],
        model="llama3-8b-8192",
        temperature=0
    )
    return chat_completion.choices[0].message.content
