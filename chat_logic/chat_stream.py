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

    Gererate a response from the model based on the user's query and chat history.
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
                
# Feedback function for thumbs up (chat ends with success message)
def feedback_positive(history):
    history.append((None, "🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask."))
    return history

# Feedback function for thumbs down (chat continues)
def feedback_negative(history):
    history.append((None, "I'm sorry to hear that. Could you describe the issue further? Maybe we can find another solution."))
    return history