#%% 
# processing functions
from rag.vectorization_functions import split_documents, create_embedding_vector_db, query_vector_db
# lead ifixit infos
from rag.ifixit_document_retrieval import load_ifixit_guides
#model
from helper_functions.llm_base_client import llm_base_client_init
from chat_logic.prompts import load_prompts
import time
import gradio as gr

def chatbot_answer(user_query, memory=None,  context="", prompt="default", response_type=None, modelname="llama3-8b-8192", temp=0.3):
    """ 

    Generate a response from the model based on the user's query and chat history.
    Can be used for both the first query and follow-up questions by using different prompts.

    Args:
        user_query (str): The user's query.
        memory (list): The chat history.
        context (str): The context to use in the prompt.
        prompt (str): The prompt to load.
        response_type (str): The style of language the answer should use.
        modelname (str): The name of the model to use.
        temp (float): The temperature for the model.

    Returns:
        str: The model's response.
    
    """
    client = llm_base_client_init()
    answer_prompt = load_prompts(prompt, context, response_type)
    messages = [{"role": "system",
              "content": answer_prompt}]
    
    if memory:
        for user_msg, bot_msg in memory:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": user_query})

    # calling the LLM with the entire chat history in order to get an answer
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=modelname,
        temperature=temp
    )
    return chat_completion

def chatbot_answer_init(user_query, vector_db, history, response_type, prompt):
    """
    Generate the answer for the answer for the query.

    Args:
        user_query (str): The user's query.
        vector_db: The vector database to query.
        history (list): The chat history.
        response_type (str): The style of language the answer should use.
        prompt (str): The prompt to load.
    returns:
        answer (list): The model's response added to the chat history.
    """
    context = query_vector_db(user_query, vector_db)
    message_content = chatbot_answer(user_query, history, context, prompt, response_type)
    answer = history + [(user_query, message_content.choices[0].message.content)]
    return answer

def chatbot_rag_init(user_query):
    """
    Create the vector database for the first query.
    This function loads the guides, splits them into chunks, and creates the embedding vector database.
    """
    
    data = load_ifixit_guides(user_query, debug=True)
    chunks = split_documents(data)
    vector_database = create_embedding_vector_db(chunks)
    return vector_database

def chatbot_interface(history, user_query, response_type):
    """ 

    UI uses this function to handle general chat functionality. 
    Order of operations is also defined here.

    Args:
        history (list): The chat history.
        user_query (str): The user's query.
        response_type (str): The style of language the answer should use.
    
    Returns:
        list: The model's response added to the chat history.
    
    """

    # load guides, create embeddings and return answer for first query
    if len(history) == 0:
        global vector_db
        vector_db = [] # reset vector database to avoid memory issues
        vector_db = chatbot_rag_init(user_query)
        answer = chatbot_answer_init(user_query, vector_db, history, response_type, prompt="repair_guide")
    # answer questions to the guide 
    else: 
        answer = chatbot_answer_init(user_query, vector_db, history, response_type, prompt="repair_helper")
    
    return answer

# Feedback function for thumbs up (chat ends with success message & restarts)
def feedback_positive(history):
    history.append([None, "🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask. I will automatically restart the chat."])
    print("Chat history:", history)
    yield history, gr.update(value="") # shows message
    time.sleep(5) # short break for message to remain
    history.clear()
    print("History after clearing:", history) 
    yield [], gr.update(value="") # reset chat


# Feedback function for thumbs down (chat restarts)
# def feedback_negative(history):
#     history.append((None, "I'm sorry to hear that. Do you want me to create a support ticket for you so that you can seek professional help?"))
#     print("Chat history:", history)
#     yield history, gr.update(value="") # shows message
#     time.sleep(5) # short break for message to remain
#     history.clear()
#     print("History after clearing:", history) 
#     yield [], gr.update(value="") 

# NEW Feedback function for thumbs down
def feedback_negative(history):
    history.append((None, "I'm sorry to hear that. Do you want me to create a support ticket for you so that you can seek professional help?"))
    print("Chat history:", history)
    yield history, "awaiting_support_confirmation"

# NEW Feedback function for thumbs down (chat continues)
def support_ticket_needed(message, history, state):
    user_message = message.strip().lower()
    history.append((message, "test"))

    if state == "awaiting_support_confirmation":
        if "yes" in user_message:
            history.append((None, "🛠️ Your individual support ticket is created."))
            yield history, "", "normal"
        elif "no" in user_message:
            history.append((None, "👍 Ok, I would be happy to help with the next repair problem."))
            yield history, "", "normal" # shows message
            time.sleep(5) # short break for message to remain
            history.clear()
            yield [], "", "normal" # reset chat
        else:
            history.append((None, "❓ Please answer with yes or no."))
            yield history, "", "awaiting_support_confirmation"

# NEW WIP: support ticket creation
# def support_ticket_needed(message, history, state):
#     user_message = message.strip().lower()
#     history.append([message, None])

#     if state == "awaiting_support_confirmation":
#         if "yes" in user_message:
#             # Extrahiere den bisherigen Verlauf als Kontext
#             context = "\n".join([f"User: {msg[0]}\nAssistant: {msg[1]}" for msg in history if msg[0] and msg[1]])
#             # Generiere den Prompt für das Support-Ticket
#             ticket_prompt = load_prompts(prompt="support_ticket", context=context)
#             # Initialisiere den LLM-Client
#             client = llm_base_client_init()
#             # Erstelle das Support-Ticket
#             ticket_response = client.chat.completions.create(
#                 messages=[{"role": "system", "content": ticket_prompt}],
#                 model="llama3-8b-8192",
#                 temperature=0.3
#             )
#             ticket_text = ticket_response.choices[0].message.content
#             # Füge das generierte Ticket dem Verlauf hinzu
#             history.append((None, f"🛠️ Your support ticket has been created:\n\n{ticket_text}"))
#             yield history, "", "normal"
#         elif "no" in user_message:
#             history.append((None, "👍 Ok, I would be happy to help with the next repair problem."))
#             yield history, "", "normal"
#             time.sleep(5)
#             history.clear()
#             yield [], "", "normal"
#         else:
#             history.append((None, "❓ Please answer with yes or no."))
#             yield history, "", "awaiting_support_confirmation"
