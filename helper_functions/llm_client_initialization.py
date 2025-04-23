import os
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq

def llm_base_client_init():
    """
    Initializes the LLM client from the groq package with personal API key
    
    Args:
          no input needed
    
    Returns:
          the Groq client
    """
    load_dotenv()
    groq_key = os.getenv('GROQ_API_KEY')
    client = Groq(api_key=groq_key)

    return client

def llm_langchain_client_init(modelname="llama-3.1-8b-instant", temp=0.2):
    '''
    Initializes the LLM client using the langchain_groq package with personal API key
    
    Args:
           modelname (str): The name of the model to use. "llama-3.1-8b-instant" is default.  
           Another potential models is "meta-llama/llama-4-scout-17b-16e-instruct"
           temp (float): The temperature for the model.
    
    Returns:
            ChatGroq client (obj)
    
    '''
    load_dotenv()
    groq_key = os.getenv('GROQ_API_KEY')

    client = ChatGroq(
        model=modelname,
        temperature=temp,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=groq_key
        )
    return client