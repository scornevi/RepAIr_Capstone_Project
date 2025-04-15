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
    
    elif prompt == "repair_guide":
        prompt = (f"List repair steps for the Problem. Use the following context:\n{context}. " + response_type)
    
    elif prompt == "repair_helper":
        prompt = (f"Answer the users question about the guide. Use the following context:\n{context}. " + response_type)

# NEW: Create support ticket
    elif prompt == "support_ticket":
        prompt = ("""
                    You are a technical support assistant. Based on the user's input, generate a structured support ticket with the following fields:
                    1. Device Type
                    2. Brand and Model
                    3. Serial Number (if available)
                    4. Date of Purchase
                    5. Problem Description
                    6. Troubleshooting Steps Already Taken
                    7. Occurrence Frequency
                    8. Additional Notes (if available)

                    Ensure the ticket is clear and concise, suitable for submission to a professional repair service.

                    User Input:\n
                    {context}
                    """ + response_type)
        
    return prompt