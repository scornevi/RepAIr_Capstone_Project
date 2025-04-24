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

def chatbot_answer(user_query, memory=None, context="", prompt="default", response_type=None, modelname="llama3-8b-8192", temp=0.3):
    """ 

    Generate a response from the model based on the user's query and chat history.

    Args:
        user_query (str): The user's query.
        memory (list): The chat history. List of tuples.
        context (str): The context to use in the prompt. Context is usually the vector DB chunks returned by the similarity search.
        prompt (str): The prompt to load.
        response_type (str): The style of language the answer should use.
        modelname (str): The name of the model to use.
        temp (float): The temperature for the model.

    Returns:
        chat_completion (str): The model's response.
    
    """
    # Initialize the LLM client
    client = llm_base_client_init()
    # Load the prompt
    answer_prompt = load_prompts(prompt, context, response_type)

    # Create the messages for the chat completion
    # The system message is the prompt that the model will use to generate a response.
    messages = [{"role": "system",
              "content": answer_prompt}]
    
    if memory:
        # unpacking the chat history from the list of tuples and appending them to the message list
        for user_msg, bot_msg in memory:
            if user_msg and user_msg != None:
                messages.append({"role": "user", "content": user_msg})
            if bot_msg:
                messages.append({"role": "assistant", "content": bot_msg})
    # last message is the user query
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
        vector_db: The vector database to query. Populated only after the iFixIt guides have been loaded.
        history (list): The chat history. List of tuples.
        response_type (str): The style of language the answer should use.
        prompt (str): The prompt to load.
        k (int): The number of chunks to return from the vector database.
        modelname (str): The name of the model to use.
        temp (float): The temperature for the model.
        history_length (int): The number of messages to include from the chat history.

    Returns:
        answer (list): The model's response added to the chat history.
    """
    # Check if the vector database is empty or None and populate context if vector_db is not None
    if vector_db:
        context = query_vector_db(user_query, vector_db, k)
    else:
        context = ""

    # Calling chat completion with the user query, context, and chat history and adding answer to the history
    message_content = chatbot_answer(user_query, history[-(history_length):], context, prompt, response_type, modelname, temp)
    answer = history + [[user_query, message_content.choices[0].message.content]]
    return answer

def chatbot_rag_init(user_query):
    """
    Create the vector database for the first query.
    This function loads the guides, splits them into chunks, and creates the embedding vector database.

    Args:
        user_query (str): The user's query.
    
    Returns:
        vector_database: The vector database created from the iFixIt guides.
    """
    # Load the iFixIt guides and create the vector database
    data = load_ifixit_guides(user_query, debug=True)
    chunks = split_documents(data)
    vector_database = create_embedding_vector_db(chunks)
    return vector_database

def chatbot_interface(history, user_query, response_type, conversation_state):
    """ 

    UI uses this function via handle input to handle general chat functionality.
    Chat logic is defined here depending on the conversation state (interactive diagnosis or repair mode).

    Args:
        history (list): The chat history.
        user_query (str): The user's query.
        response_type (str): The style of language the answer should use.
        conversation_state (str): The current state of the conversation before the user query
    
    Returns:
        answer (list): The model's response added to the chat history.
        conversation_state (str): The state of the conversation after the current user query
    
    """

    if conversation_state == 'interactive_diagnosis':
    #If in status interactive_diagnosis, get answer from chatbot and extract information from the answer
        answer = chatbot_answer_init(user_query, None, history, response_type, prompt="diagnose_issue")
        extracted_info = information_extractor(answer)
        # When extracting information, system sometimes populates the fields with invalid information (None, not specified, etc.)
        # even though no information was provided by the user. This is a workaround to check if the fields are empty or invalid
        # and to remain in conversation state interactive_diagnosis until the user provides valid information.
        if any(value == '' or value is None or (value is not None and 'none' in value.lower()) or 
            (value is not None and 'not specified' in value.lower()) or 
            (value is not None and 'unknown' in value.lower() or (value is not None and 'no specific' in value.lower()))
            for value in extracted_info.values()
            ):
            conversation_state = "interactive_diagnosis"
        else:
            # if the information is valid, create the vector database
            global vector_db
            vector_db = [] # reset vector database to avoid memory issues
            vector_db = chatbot_rag_init(answer[-1][1])
            # Create the repair question based on the extracted information
            repair_question = f"List repair steps for {extracted_info['issue']} of {extracted_info['brand']} {extracted_info['model']}."
            # Query chatbot with the repair question and the vector database
            answer = chatbot_answer_init(repair_question,
                                         vector_db,
                                         history,
                                         response_type,
                                         prompt="repair_guide",
                                        k=10,
                                        modelname="llama-3.1-8b-instant",
                                        temp=0.3)
            # Change conversation state to repair mode to indicate that the interactive diagnosis is done and the repair mode is active
            conversation_state = "repair_mode"

    elif conversation_state == 'repair_mode':
        answer = chatbot_answer_init(user_query,
                                    vector_db,
                                    history,
                                    response_type,
                                    prompt="repair_helper",
                                    k=5)
    # load guides, create embeddings and return answer for first query
    print("Answer before returning to Handle User Input:", answer) # logs to show the answer before returning to the UI. Can be commented out if not needed.
    return answer, conversation_state

def handle_user_input(user_input_text, history, conversation_state, response_type):
    """
    Handle user input and determine the next steps based on the conversation state. This function is called by the UI to
    route the user input to the support ticket needed function if the user clicked "thumbs down", which sets the conversation state to "awaiting_support_confirmation".

    Args:
        user_input_text (str): The user's input text.
        history (list): The chat history.  List of tuples.
        conversation_state (str): The current state of the conversation before the user input.
        response_type (str): The style of language the answer should use.
    
    Yields:
        answer (list): The model's response added to the chat history.
        user_input (str): string to set the input box to empty after the user input is processed.
        conversation_state (str): The state of the conversation after the current user input.

    """
    print("Conversation state before calling Chatbot Interface:", conversation_state) # logs to show the conversation state before calling the chatbot interface. Can be commented out if not needed.
    print("History before calling Chatbot Interface:", history) # logs to show the chat history before calling the chatbot interface. Can be commented out if not needed.

    if conversation_state == "awaiting_support_confirmation":
        # If the user clicked "thumbs down", call the support ticket needed function to check whether the user wants to create a support ticket or not
        # based on the user input text.
        yield from support_ticket_needed(user_input_text, history, conversation_state)
    else:
        # Default logic if the user clicked "Submit" or entered a message in the chat box and did not click "thumbs down" beforehand.
        answer, conversation_state = chatbot_interface(history, user_input_text, response_type, conversation_state)
        print("Answer before returning to Interface Design:", answer) # logs to show the answer before returning to the UI. Can be commented out if not needed.
        print("Conversation state before returning to Interface Design:", conversation_state) # logs to show the conversation state before returning to the UI. Can be commented out if not needed.
        yield answer, "", conversation_state

# Feedback function for thumbs up (chat ends with success message & restarts)
def feedback_positive(history):
    """ This function is called when the user clicks "thumbs up" to indicate that the repair was successful.

    Args:
        history (list): The chat history.  List of tuples.

    Yields:
        answer (list): The model's response added to the chat history or an empty list to reset the chat
        user_input (str): string to set the input box to empty after the user input is processed.
        conversation_state (str): The state of the conversation after the current user input.
    """
    # Append a success message to the chat history
    # and set the conversation state to "repair_helper" to indicate that the chat is in repair mode.
    history.append([None, "<br><br><br>🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask. I will automatically restart the chat."])
    print("Chat history:", history)
    conversation_state = "repair_helper"
    yield history, gr.update(value=""), conversation_state # shows message
    # Wait for a short time to allow the message to be displayed before clearing the chat history
    # and resetting the conversation state to "interactive_diagnosis" to indicate that the chat is ready for a new diagnosis.
    time.sleep(5) # short break for message to remain
    history.clear()
    conversation_state = "interactive_diagnosis"
    print("History after clearing:", history) # logs to show the chat history after clearing. Can be commented out if not needed.
    yield [], gr.update(value=""), conversation_state # reset chat

# Feedback function for thumbs down
def feedback_negative(history):
    """ This function is called when the user clicks "thumbs down" to indicate that the repair was not successful.

    Args:
        history (list): The chat history.  List of tuples.

    Yields:
        history: (list): The chat history with the thumbs down message appended.
        conversation_state (str): The state of the conversation after the current user input.
    """
    # Append a thumbs down message to the chat history
    history.append((None, "<br><br><br>I'm sorry to hear that. Do you want me to create a support ticket for you so that you can seek professional help?"))
    print("Chat history:", history) # logs to show the chat history after thumbs down. Can be commented out if not needed.
    # Set the conversation state to "awaiting_support_confirmation" to indicate that the chat is waiting for the user's confirmation to create a support ticket.
    conversation_state = "awaiting_support_confirmation"
    yield history, conversation_state

# Support ticket creation
def support_ticket_needed(message, history, conversation_state):
    """ This function is called when the user clicks "thumbs down", checks whether the user wants to create a support ticket or not based on the user input text.
        and creates a support ticket if the user confirms.

    Args:
        message (str): user input text
        history (list): the chat history. List of tuples.
        conversation_state (str): conversation state before the user input

    Yields:
        answer (list): The model's response added to the chat history or an empty list to reset the chat
        user_input (str): string to set the input box to empty after the user input is processed.
        conversation_state (str): The state of the conversation after the current user input.
    """
    user_message = message.strip().lower()
    history.append((message, None))
    # Checks conversation state. Actually not required since the function is only called when the conversation state is "awaiting_support_confirmation".
    if conversation_state == "awaiting_support_confirmation":
        if "yes" in user_message:
        # If the user confirms that they want to create a support ticket, call the chatbot_answer_init function to create the support ticket.
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
        # If the user does not want to create a support ticket, append a message to the chat history indicating that the chat is ready for a new diagnosis.
            history.append((None, "👍 Ok, I would be happy to help with the next repair problem."))
            yield history, "", conversation_state
            time.sleep(5)
            # Wait for a short time to allow the message to be displayed before clearing the chat history
            history.clear()
            conversation_state = "interactive_diagnosis"
            yield history, "", conversation_state
        else:
            history.append((None, "❓ Please answer with yes or no."))
            yield history, "", conversation_state

