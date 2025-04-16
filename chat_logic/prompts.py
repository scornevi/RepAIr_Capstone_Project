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

    elif response_type == "Technical":
        response_type = "Use technical jargon and provide detailed explanations."

    elif response_type == "Homer Simpson Language":
        response_type = "Use simple language and explain it like Homer Simpson would."
    
    elif response_type == "Sarcasm":
        response_type = "Use sarcastic language and tone."
    
    elif response_type is None:
        response_type = ""

    # choose prompt and append response_type
    if prompt == "default":
        prompt = ("""You are a helpful assistant that helps users with the repair of their devices.
                  Ask them if they need help with a repair.
                  If they do, ask them to provide the device name and model. """ + response_type)
        
    elif prompt == "diagnose_issue":
        prompt = ("""
                You are a helpful assistant.
                Your job is to determine if an appliance or device, the brand of the appliance or device,
                the model of the appliance or device and the user's issue with the applicance or device
                were mentioned in the user's message.
                If yes, extract the appliance or device, its model and its issue and confirm it back to the user and stop asking for information.
                If not, continue to ask the user to provide the missing information until they provide it.
                Do not provide troubleshooting steps or solutions.""" + response_type)
    
    elif prompt == "repair_guide":
        prompt = (f"List repair steps for the Problem. Use the following context:\n{context}. " + response_type)
    
    elif prompt == "repair_helper":
        prompt = (f"Answer the users question about the guide. Use the following context:\n{context}. " + response_type)
    
    return prompt
