def load_prompts(prompt, context="", response_type=None):
    """
    Load the prompts from a file or define them in the code.

    """
    
    
    # choose response_type
    if response_type == "Simple Language":
        response_type = "Use plain language and explain so that a 5th grader would understand."

    if response_type == "Technical":
        response_type = "Use technical jargon and provide detailed explanations."

    if response_type == "Homer Simpson Language":
        response_type = " Use simple language and explain it like Homer Simpson would."
    
    if response_type == "Sarcasm":
        response_type = "Use sarcastic language and tone."
    
    if response_type is None:
        response_type = ""

    # choose prompt

    if prompt == "default":
        prompt = ("""You are a helpful assistant that helps users with the repair of their devices.
                  Ask them if they need help with a repair.
                  If they do, ask them to provide the device name and model."""+response_type)
    
    if prompt == "repair_guide":
        prompt = (f"List repair steps for the Problem. Use the following context:\n{context}"+ response_type)
    
    if prompt == "repair_helper":
        prompt = (f"Answer the users question about the guide. Use the following context:\n{context}"+ response_type)

    return prompt

   
    
    