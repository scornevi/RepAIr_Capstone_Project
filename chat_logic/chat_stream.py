#%% 
# processing functions
from rag.vectorization_functions import split_documents, create_embedding_vector_db, query_vector_db
# lead ifixit infos
from rag.ifixit_document_retrieval import load_ifixit_guides
#model
from helper_functions.llm_base_client import llm_base_client_init
from chat_logic.prompts import load_prompts

def chatbot_answer(user_query, context="", prompt="default", modelname="llama3-8b-8192", temp=0.3):
    """ 

    LLM Model is defined here.
    Chat history use and chat with user coded here.
    
    """
    client = llm_base_client_init()
    answer_prompt = load_prompts(prompt, context)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
              "content": answer_prompt},
            {"role": "user", "content": user_query},
        ],
        model=modelname,
        temperature=temp
    )
    return chat_completion


def chatbot_interface(history, user_query):
    """ 

    LLM Model is defined here.
    Chat history use and chat with user coded here.
    
    """

    # load guides, create embeddings and return answer for first query
    if len(history) == 0:
        data = load_ifixit_guides(user_query, debug=True)
        chunks = split_documents(data)
        global vector_db
        vector_db = create_embedding_vector_db(chunks)
        context = query_vector_db(user_query, vector_db)
        message_content = chatbot_answer(user_query, context, prompt="repair_guide")
        answer = history + [(user_query, message_content.choices[0].message.content)]
        return answer
    
    # answer questions to the guide 
    else: 
        context = query_vector_db(user_query, vector_db)
        message_content = chatbot_answer(user_query, context, prompt="repair_helper")
        answer = history + [(user_query, message_content.choices[0].message.content)]
        return answer

                    

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