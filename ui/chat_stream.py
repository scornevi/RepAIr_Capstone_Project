
# processing functions
from rag.vectorization_functions import split_documents, create_embedding_vector_db, rewrite_query, query_vector_db
# lead ifixit infos
from rag.ifixit_document_retrieval import load_data


def chatbot_interface(history, user_query):
    """ 
    LLM Model is defined here.
    Chat history use and chat with user coded here.
    
    """
    
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
    
    data = load_data()
    chunks = split_documents(data)
    vector_db = create_embedding_vector_db(chunks)
    
    optimized_query = rewrite_query(user_query)
    return history + [(user_query, query_vector_db(optimized_query, vector_db))]