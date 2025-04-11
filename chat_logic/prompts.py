def load_prompts(prompt="default", context="", response_type=None):
    """
    Load the prompts from a file or define them in the code.

    Args:
        prompt (str): The prompt to load.
        context (str): The context to use in the prompt.
        response_type (str): The style of language the answer should use.

    Returns: 
        str: The loaded prompt.

    """
 
    # choose response_type
    if response_type == "Simple Language":
        response_type = "Use plain language and explain so that a 5th grader would understand."

    if response_type == "Technical":
        response_type = "Use technical jargon and provide detailed explanations."

    if response_type == "Homer Simpson Language":
        response_type = "Use simple language and explain it like Homer Simpson would."
    
    if response_type == "Sarcasm":
        response_type = "Use sarcastic language and tone."
    
    if response_type is None:
        response_type = ""

    # choose prompt and append response_type
    if prompt == "default":
        prompt = ("""You are a helpful assistant that helps users with the repair of their devices.
                  Ask them if they need help with a repair.
                  If they do, ask them to provide the device name and model. """ + response_type)
    
    if prompt == "repair_guide":
        prompt = (f"List and explain the repair steps mentioned in the guide. Use the following context:\n{context}. " + response_type)
    
    if prompt == "repair_helper":
        prompt = (f"Answer the users question about the guide. Use the following context:\n{context}. " + response_type)
    
    if prompt == "check_info":
        prompt = ("""Write 'yes' if device name, model and problem description containing a faulty part are provided, otherwise return 'no'.
                  Only return 'yes' or 'no' without any comments or explanations.
                  """)
        
    if prompt == "need_more_info":
        prompt = ("""You need to get information from the user to start a repair. For this you need the following information:
                  Device name, model, problem description with faulty part.
                  Ask the user to provide the missing information. 
                  """)
    if prompt == "summary":
        prompt = ("""Summarize the history and user input. 
                  It should be a short sentence that describes the problem and contains the following information:
                  Device name, model and problem description that contains the faulty part.
                  Only write one sentence without any comments and explanations.
                  Always use the order: Device name, model, problem description.
                  """)

    return prompt

   
    
    