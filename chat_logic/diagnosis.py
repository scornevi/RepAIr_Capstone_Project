#%% 
# processing functions
# lead ifixit infos

from langchain.chat_models import init_chat_model
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
# import langchain groq package
from helper_functions.llm_client_initialization import llm_langchain_client_init
import re


def information_extractor(conversation):
    """
    Extracts the device, brand, model and issue from the conversation using a language model.
    Input: entire diagnosis conversation between bot and user
    Output: dictionary with device, brand, model and issue
    """
    # Initializing the Grog Client
    llm = llm_langchain_client_init()
    # Defining the information we want to extract from the response
    schemas = [
        ResponseSchema(name="device", description="Device or appliance mentioned, if any"), # one line per information that we are trying to extract
        ResponseSchema(name="brand", description="Brand of device or appliance mentioned, if any"), # one line per information that we are trying to extract
        ResponseSchema(name="model", description="Model of device or appliance mentioned, if any"), # one line per information that we are trying to extract
        ResponseSchema(name="issue", description="Main issue or concern with device or appliance, if any. Leave empty if none.")
        ]
    
    # Initialization of the parser
    parser = StructuredOutputParser.from_response_schemas(schemas)

    print(parser)

    # Defining the chat prompt template
    prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the following info from the message of the user."),
    ("user", "{text}\n\n{format_instructions}")
    ])
    
    # Defining parsing instructions for the output
    #Theoretically, the parser is to generate the parsing instructions automatically,
    # but it cannot tell the client to remove the comments in the output, which leads to errors when parsing the json downstream 
    # parsing_instructions=parser.get_format_instructions()
    parsing_instructions ='''
        The output should be a markdown code snippet formatted in the following schema,
        including the leading and trailing "```json" and "```", without any additional text or comments:

        ```json
        {
            "device": string  // Device or appliance mentioned, if any
            "brand": string  // Brand of device or appliance mentioned, if any
            "model": string  // Model of device or appliance mentioned, if any
            "issue": string  // Main issue or concern with device or appliance, if any. Leave empty if none.
        }
        ```
        '''
    
    # Formattig the prompt with last message in the conversation and instructions to parse the information from that message
    formatted_prompt = prompt.format_prompt(
    text=conversation[-1][1],  # The last message in the conversation
    format_instructions=parsing_instructions
    )

    print('Text parsed by LLM: ', conversation[-1][1])
    
    # Calling the LLM with the formatted prompt and parsing the output
    output = llm(formatted_prompt.to_messages())
    print("Output Content: " + output.content)

    cleaned_content = re.sub(r'//.*$', '', output.content, flags=re.MULTILINE)

    print("Cleanded Content: " + cleaned_content)
    
    parsed_content = parser.parse(cleaned_content)
    print("Dictionary: ", parsed_content)
    return parsed_content