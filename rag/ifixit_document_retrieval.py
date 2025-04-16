
from langchain_community.document_loaders import IFixitLoader
from helper_functions.llm_client_initialization import llm_base_client_init
#function for rewriting info into searchphrase
def write_searchphrase(search_info: str, debug: bool = False):
    """
    Uses the LLM to rewrite input into a structured searchphrase iFixit searches.

    Args:
        search_info (str): The information to be turned into a searchphrase.

    Returns:
        str: The rewritten searchphrase.
    """
    client = llm_base_client_init()
    
    chat_completion = client.chat.completions.create(
        messages=[
           {"role": "system",
             "content": """Rewrite the following info into a structured searchphrase for iFixit, 
             ensuring it includes in this order the device name, model and part that needs to be repaired. 
             Return only the searchphrase, do not include any other words or comments.
             Capitalize the first letter of each word.
             The searchphrase should be a single sentence."""},
            {"role": "user", "content": search_info},
        ],
        model="llama3-8b-8192",
        temperature=0.1
    )
    search_phrase = chat_completion.choices[0].message.content
    if debug == True:
        print('Full searchphrase:', search_phrase)
    return search_phrase

#load guides from iFixit
def load_guides(search_phrase: str, debug: bool = False):
    """
    Load a guide from IFixit based on the search phrase.
    If no guide is found, iteratively remove the last word and retry.
    
    Args:
        search_phrase (str): The phrase to search for in IFixit guides.
        
    Returns:
        guides: The loaded guide data or None if no guide is found.
    """
    words = search_phrase.split()
    
    while words:
        query = " ".join(words)
        guides = IFixitLoader.load_suggestions(query, doc_type='guide')
        
        if guides:
            if(debug == True):
                print('Used words:', words)
            return guides  # Return results if found
        
        words.pop()  # Remove the last word and retry

    print('No guides found')
    return None  # Return None if no guide is found

def load_ifixit_guides(search_info: str, debug: bool = False):
    """

    Rewrites the search info into a searchphrase and loads guides from iFixit.

    Args:
        search info (str): The information to be turned into a searchphrase.
        
    Returns:
        guides: The loaded guide data or None if no guide is found.

    """
    search_phrase = write_searchphrase(search_info, debug=debug)
    guides = load_guides(search_phrase, debug=debug)
    return guides
