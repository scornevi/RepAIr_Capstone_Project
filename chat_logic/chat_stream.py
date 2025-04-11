#%% 
# processing functions
from rag.vectorization_functions import split_documents, create_embedding_vector_db, query_vector_db
# lead ifixit infos
from rag.ifixit_document_retrieval import load_ifixit_guides
#model
from helper_functions.llm_base_client import llm_base_client_init
from chat_logic.prompts import load_prompts


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

def chatbot_answer_init(user_query, vector_db, history, response_type, prompt, modelname="llama3-8b-8192", temp=0.3):
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
        context = query_vector_db(user_query, vector_db)
    else:
        context = ""
    message_content = chatbot_answer(user_query, history, context, prompt, response_type, modelname, temp)
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
    global chat_state

    # chat until enough information is provided to answer the question
    if len(history) == 0:
        chat_state = "diagnosis"

    if chat_state == "diagnosis":
        sum_prompt = load_prompts("summary")
        summary_list = chatbot_answer(user_query, history, None, prompt=sum_prompt, response_type=None, modelname="llama3-8b-8192", temp=0.2)
        summary = str(summary_list.choices[0].message.content).strip().lower()
        print(summary)
        check_prompt = load_prompts("check_info")
        check_info = chatbot_answer(summary, [], None, prompt=check_prompt, response_type=None, modelname="llama3-8b-8192", temp=0.2)
        enough_info = str(check_info.choices[0].message.content).strip().lower()
        print(enough_info)
        if enough_info == 'yes':
            # load guides, create embeddings and return answer for first query
            global vector_db
            vector_db = [] # reset vector database to avoid memory issues
            vector_db = chatbot_rag_init(summary)
            answer = chatbot_answer_init(summary, vector_db, [], response_type, prompt="repair_guide")
            chat_state = "repair"
            return answer
        else:
            # ask for more information
            answer = chatbot_answer_init(user_query, None, history, prompt="need_more_info", response_type=response_type)
            chat_state = "diagnosis"
            return answer

    # answer questions to the guide
    if chat_state == "repair":
        answer = chatbot_answer_init(user_query, vector_db, history, response_type, prompt="repair_helper")
        return answer

                
# Feedback function for thumbs up (chat ends with success message)
def feedback_positive(history):
    history.append((None, "🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask."))
    return history

# Feedback function for thumbs down (chat continues)
def feedback_negative(history):
    history.append((None, "I'm sorry to hear that. Could you describe the issue further? Maybe we can find another solution."))
    return history