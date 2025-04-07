def load_prompts(prompt, context="", response_type=None):
    """
    Load the prompts from a file or define them in the code.

    """
    # choose prompt

    if prompt == "default":
        prompt = """You are a helpful assistant that helps users with the repair of their devices.
                  Ask them if they need help with a repair.
                  If they do, ask them to provide the device name and model."""
    
    if prompt == "repair_guide":
        prompt = (f"List repair steps for the Problem. Use the following context:\n{context}")
    
    if prompt == "repair_helper":
        prompt = (f"Answer the users question about the guide. Use the following context:\n{context}")
    
    # choose response_type
    if response_type == "Simple Language":
        prompt += " Please provide a clear and easy-to-understand explanation."

    elif response_type == "Technical":
        prompt += " Provide a detailed technical breakdown of the repair process."

    elif response_type == "Homer Simpson Language":
        prompt += " Provide an explanation of the repair process how Homer Simpson would say it."

    # return prompt

    return prompt

   
    
    