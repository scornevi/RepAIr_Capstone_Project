#%% 
# processing functions
from rag.vectorization_functions import split_documents, create_embedding_vector_db, query_vector_db
# lead ifixit infos
from rag.ifixit_document_retrieval import load_ifixit_guides
#model
from helper_functions.llm_client_initialization import llm_base_client_init
from chat_logic.prompts import load_prompts
from chat_logic.diagnosis import information_extractor
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
            if user_msg and user_msg != None:
                messages.append({"role": "user", "content": user_msg})
            if bot_msg:
                messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": user_query})

    # calling the LLM with the entire chat history in order to get an answer
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=modelname,
        temperature=temp
    )
    return chat_completion

def chatbot_answer_init(user_query, vector_db, history, response_type, prompt, k=5, modelname="llama3-8b-8192", temp=0.3, history_length=5):
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
    if vector_db:
        context = query_vector_db(user_query, vector_db, k)
    else:
        context = ""

    message_content = chatbot_answer(user_query, history[-(history_length):], context, prompt, response_type, modelname, temp)
    answer = history + [[user_query, message_content.choices[0].message.content]]
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

def chatbot_interface(history, user_query, response_type, conversation_state):
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
    #Diagnose issue
    if conversation_state == 'interactive_diagnosis':
        answer = chatbot_answer_init(user_query, None, history, response_type, prompt="diagnose_issue")
        extracted_info = information_extractor(answer)
    
        if any(value == '' or (value is not None and 'none' in value.lower()) or 
            (value is not None and 'not specified' in value.lower()) or 
            (value is not None and 'unknown' in value.lower())
            for value in extracted_info.values()
            ):
            conversation_state = "interactive_diagnosis"
        else:
            global vector_db
            vector_db = [] # reset vector database to avoid memory issues
            vector_db = chatbot_rag_init(answer[-1][1])

            repair_question = f"List repair steps for {extracted_info['issue']} of {extracted_info['brand']} {extracted_info['model']}."

            answer = chatbot_answer_init(repair_question,
                                         vector_db,
                                         history,
                                         response_type,
                                         prompt="repair_guide",
                                        k=10,
                                        modelname="llama-3.1-8b-instant",
                                        temp=0.3)
            conversation_state = "repair_mode"

    elif conversation_state == 'repair_mode':
        answer = chatbot_answer_init(user_query,
                                    vector_db,
                                    history,
                                    response_type,
                                    prompt="repair_helper",
                                    k=5)
    # load guides, create embeddings and return answer for first query
    print("Answer before returning to Handle User INput:", answer)
    return answer, conversation_state

def handle_user_input(user_input_text, history, conversation_state, response_type):
    print(conversation_state)
    print(type(conversation_state))
    print("History before calling Chatbot Interface:", history)

    if conversation_state == "awaiting_support_confirmation":
        yield from support_ticket_needed(user_input_text, history, conversation_state)
    else:
        answer, conversation_state = chatbot_interface(history, user_input_text, response_type, conversation_state)
        print("Answer before returning to Interface Design:", answer)
        print("Conversation state before returning to Interface Design:", conversation_state)
        yield answer, "", conversation_state

# Feedback function for thumbs up (chat ends with success message & restarts)
def feedback_positive(history):
    history.append([None, "<br><br><br>🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask. I will automatically restart the chat."])
    print("Chat history:", history)
    conversation_state = "repair_helper"
    yield history, gr.update(value=""), conversation_state # shows message
    time.sleep(5) # short break for message to remain
    history.clear()
    conversation_state = "interactive_diagnosis"
    print("History after clearing:", history) 
    yield [], gr.update(value=""), conversation_state # reset chat

# Feedback function for thumbs down
def feedback_negative(history):
    history.append((None, "<br><br><br>I'm sorry to hear that. Do you want me to create a support ticket for you so that you can seek professional help?"))
    print("Chat history:", history)
    conversation_state = "awaiting_support_confirmation"
    yield history, conversation_state

# Support ticket creation
def support_ticket_needed(message, history, conversation_state):
    user_message = message.strip().lower()
    history.append((message, None))
    if conversation_state == "awaiting_support_confirmation":
        if "yes" in user_message:
            ticket_text = chatbot_answer_init("Please summarize this history into a support ticket.",
                                            vector_db,
                                            history,
                                            response_type="Technical",
                                            prompt="support_ticket",
                                            history_length=len(history)
                                            )
            history.append((None, f"🛠️ Your support ticket has been created:\n\n{ticket_text[-1][1]}"))
            conversation_state = "repair_helper"
            yield history, "", conversation_state
        elif "no" in user_message:
            history.append((None, "👍 Ok, I would be happy to help with the next repair problem."))
            yield history, "", conversation_state
            time.sleep(5)
            history.clear()
            conversation_state = "interactive_diagnosis"
            yield history, "", conversation_state
        else:
            history.append((None, "❓ Please answer with yes or no."))
            yield history, "", conversation_state

