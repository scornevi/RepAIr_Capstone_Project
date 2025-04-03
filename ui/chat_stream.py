#%% 
# processing functions
from rag.vectorization_functions import split_documents, create_embedding_vector_db, query_vector_db
# lead ifixit infos
from rag.ifixit_document_retrieval import load_ifixit_guides
#model
from helper_functions.llm_base_client import llm_base_client_init


def chatbot_interface(history, user_query):
    """ 

    LLM Model is defined here.
    Chat history use and chat with user coded here.
    
    """
    
    if not user_query.strip():
        return history + [(user_query, "Hey, I'd love to help you! What can I do for you?")]
    
    client = llm_base_client_init()
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
              "content": """You are a helpful assistant 
              that helps users with the repair of their devices. Ask them if they need help with a repair.
              If they do, ask them to provide the device name and model."""},
            {"role": "user", "content": user_query},
        ],
        model="llama3-8b-8192",
        temperature=0
    )
    needs_repair_assistance = "yes" in chat_completion.choices[0].message.content.lower()
    
    if not needs_repair_assistance:
        return history + [(user_query, chat_completion.choices[0].message.content)]   
    
    data = load_ifixit_guides("iPhone 6 Screen Replacement")
    chunks = split_documents(data)
    vector_db = create_embedding_vector_db(chunks)
    
    return history + [(user_query, query_vector_db(user_query, vector_db))]