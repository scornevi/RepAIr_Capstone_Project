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
    
    messages = [{"role": "system",
              "content":  """You are a helpful assistant 
              that helps users with the repair of their devices. Ask them if they need help with a repair.
              If they do, ask them to provide the device name and model."""}]
    
    if history:
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": user_query})
    print(messages)

    client = llm_base_client_init()

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
        temperature=0.3
    )

    return history + [(user_query, chat_completion.choices[0].message.content)]  

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

    Chat history use and chat with user coded here.
    
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


def chatbot_interface(history, user_query, response_type=None):
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
        message_content = chatbot_answer(user_query, history, context, prompt="repair_guide", response_type=response_type)
        answer = history + [(user_query, message_content.choices[0].message.content)]
        return answer
    
    # answer questions to the guide 
    else: 
        context = query_vector_db(user_query, vector_db)
        message_content = chatbot_answer(user_query, history, context, prompt="repair_helper", response_type=response_type)
        answer = history + [(user_query, message_content.choices[0].message.content)]
        return answer

                    

# Feedback function for thumbs up (chat ends with success message)
def feedback_positive(history):
    history.append((None, "🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask."))
    return history

# Feedback function for thumbs down (chat continues)
def feedback_negative(history):
    history.append((None, "I'm sorry to hear that. Could you describe the issue further? Maybe we can find another solution."))
    return history