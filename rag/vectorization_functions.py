# vectorization functions
#%%
# General
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def split_documents(documents, chunk_size=800, chunk_overlap=80): # check chunk size and overlap for our purpose
    """
    This function splits documents into chunks of given size and overlap.

    Args:
        documents (list): List of documents to be split.
        chunk_size (int): Size of each chunk.
        chunk_overlap (int): Overlap between chunks.
    
    Returns:    
        list: List of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents=documents)
    return chunks

def create_embedding_vector_db(chunks):
    """
    Uses the open-source embedding model HuggingFaceEmbeddings 
    to create embeddings and store those in a vector database called FAISS, 
    which allows for efficient similarity search

    Args:
        chunks (list): List of text chunks to be embedded.
    
    Returns:
        vector_db: The vector database containing the embedded chunks.
    """
    # instantiate embedding model
    embedding = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2' # EMBEDDING MODEL! converts text to vector ( stick to it)
    )
    # create the vector store 
    vector_database = FAISS.from_documents( # stores embeddings # from_documents includes metadata
        documents=chunks,
        embedding=embedding
    )
    return vector_database # optimize

# Function to query the vector database and interact with Groq
def query_vector_db(query, vector_db):
    """
    This function queries the vector database with the user query and retrieves relevant documents

    Args:
        query (str): The user query.
        vector_db: The vector database to query.
    
    Returns:
        str: The context retrieved from the vector database.

    """
    # Retrieve relevant documents
    docs = vector_db.similarity_search(query, k=3) # neigbors k are the chunks # similarity_search: FAISS function
    context = "\n".join([doc.page_content for doc in docs])

    return context

