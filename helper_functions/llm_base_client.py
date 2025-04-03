#%%
import os
from dotenv import load_dotenv
from groq import Groq

def llm_base_client_init():
    load_dotenv()
    groq_key = os.getenv('GROQ_API_KEY')
    client = Groq(api_key=groq_key)

    return client

