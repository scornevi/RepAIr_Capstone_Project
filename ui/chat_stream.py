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
        temperature=0.3
    )
    needs_repair_assistance = "yes" in user_query.lower()
    
    if not needs_repair_assistance:
        return history + [(user_query, chat_completion.choices[0].message.content)]   
    
    data = load_ifixit_guides(user_query, debug=True)
    chunks = split_documents(data)
    vector_db = create_embedding_vector_db(chunks)
    
    return history + [(user_query, query_vector_db(user_query, vector_db))]

# Not implemented yet:
def answer_style(history, user_query, response_type):
    response = f"Suggested repair steps for: {user_query}\n\n"
    if response_type == "Simple Language":
        response += "Please provide a clear and easy-to-understand explanation."
    elif response_type == "Technical":
        response += "Provide a detailed technical breakdown of the repair process."
    
    history.append((user_query, response))  # Append to chat history
    return history


# Feedback function for thumbs up (chat ends with success message)
def feedback_positive(history):
    history.append((None, "🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask."))
    return history

# Feedback function for thumbs down (chat continues)
def feedback_negative(history):
    history.append((None, "I'm sorry to hear that. Could you describe the issue further? Maybe we can find another solution."))
    return history