# vectorization functions
#%%
# General
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from helper_functions.llm_base_client import llm_base_client_init

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

    client = llm_base_client_init() 
    # Interact with Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": f"List repair steps for the Problem. Use the following context:\n{context}"},
            {"role": "user", "content": query},
        ],
        model="llama3-8b-8192",
        temperature=0.3 # optional: check best value!
    )
    return chat_completion.choices[0].message.content
