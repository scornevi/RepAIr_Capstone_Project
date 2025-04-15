#%% 
# processing functions
from rag.vectorization_functions import split_documents, create_embedding_vector_db, query_vector_db
# lead ifixit infos
from rag.ifixit_document_retrieval import load_ifixit_guides, load_guides, write_searchphrase_from_dict
#model
from helper_functions.llm_base_client import llm_base_client_init
from chat_logic.prompts import load_prompts
from langchain.chat_models import init_chat_model
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
# import langchain groq package
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from groq import Groq

import re


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

def chatbot_smalltalk(conversation):
    """
    Extracts the device, brand, model and issue from the conversation using a language model.
    """
    load_dotenv()
    groq_key = os.getenv('GROQ_API_KEY')

    # Initializing the Grog Client
    llm = ChatGroq(
        #model="meta-llama/llama-4-scout-17b-16e-instruct",
        model="llama-3.1-8b-instant", # using a language model that is more appropriate for information extract
        temperature=0.2,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=groq_key
        )

    # Defining the information we want to extract from the response
    schemas = [
        ResponseSchema(name="device", description="Device or appliance mentioned, if any"), # one line per information that we are trying to extract
        ResponseSchema(name="brand", description="Brand of device or appliance mentioned, if any"), # one line per information that we are trying to extract
        ResponseSchema(name="model", description="Model of device or appliance mentioned, if any"), # one line per information that we are trying to extract
        ResponseSchema(name="issue", description="Main issue or concern with device or appliance, if any. Leave empty if none.")
        ]
    
    # Initialization of the parser
    parser = StructuredOutputParser.from_response_schemas(schemas)

    # Defining the chat prompt template
    prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the following info from the message of the user."),
    ("user", "{text}\n\n{format_instructions}")
    ])
    # Format and run
    parsing_instructions = '''
        The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```", without any additional text or comments:

        ```json
        {
            "device": string  // Device or appliance mentioned, if any
            "brand": string  // Brand of device or appliance mentioned, if any
            "model": string  // Model of device or appliance mentioned, if any
            "issue": string  // Main issue or concern with device or appliance, if any. Leave empty if none.
        }
        ```
        '''
    #parsing_instructions=parser.get_format_instructions()
    
    # FOrmattig the prompt with last message in the conversation and instructions to parse the information from that message
    formatted_prompt = prompt.format_prompt(
    text=conversation[-1][1],  # The last message in the conversation
    format_instructions=parsing_instructions
    )
    print('Format instructions: ', parser.get_format_instructions())
    print('Text: ', conversation[-1][1])
    
    # Calling the LLM with the formatted prompt and parsing the output
    output = llm(formatted_prompt.to_messages())
    print("Output Content: " + output.content)
    #print(str(output.content).replace("'", '"'))
    parsed = parser.parse(output.content)
    print("Dictionary: ", parsed)
    return parsed

def chatbot_diagnose_issue(history, user_query, response_type):
    """
    Have a conversation with the user to determine the appliance or device, its model and the user's issue with it.
    """
    client = llm_base_client_init()
    system_message = [{
    "role": "system",
    "content": ('''
        You are a helpful assistant.
        Your job is to determine if an appliance or device, the brand of the appliance or device,
        the model of the appliance or device and the user's issue with the applicance or device
        were mentioned in the user's message. 
        If yes, extract the appliance or device, its model and its issue and confirm it back to the user and stop asking for information.
        If not, continue to ask the user to provide the missing information until they provide it.
        Do not provide troubleshooting steps or solutions.'''
    )}]
    messages = system_message
    if history:
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": user_query})
    

    # calling the LLM with the entire chat history in order to get an answer
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
        temperature=0.3
    )
    answer = history + [(user_query, chat_completion.choices[0].message.content)]
    return answer



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

    answer = chatbot_diagnose_issue(history, user_query, response_type)
    summary = chatbot_smalltalk(answer)
    print(summary)
    if any(value == '' or 'none' in value.lower() or 'not specified' in value.lower() or 'unknown' in value.lower() for value in summary.values()):
        pass
    else:
        searchphrase = write_searchphrase_from_dict(search_info = summary)
        guides = load_guides(searchphrase, debug=True)


    # load guides, create embeddings and return answer for first query
    # if len(history) == 0:
    #     global vector_db
    #     vector_db = [] # reset vector database to avoid memory issues
    #     vector_db = chatbot_rag_init(user_query)
    #     answer = chatbot_answer_init(user_query, vector_db, history, response_type, prompt="repair_guide")
    # # answer questions to the guide 
    # else: 
    #     answer = chatbot_answer_init(user_query, vector_db, history, response_type, prompt="repair_helper")

    return answer
                
# Feedback function for thumbs up (chat ends with success message)
def feedback_positive(history):
    history.append((None, "🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask."))
    return history

# Feedback function for thumbs down (chat continues)
def feedback_negative(history):
    history.append((None, "I'm sorry to hear that. Could you describe the issue further? Maybe we can find another solution."))
    return history