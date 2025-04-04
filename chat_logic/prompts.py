def load_prompts(prompt, context=""):
    """
    Load the prompts from a file or define them in the code.

    """
    # You can load these prompts

    if prompt == "default":
        return """You are a helpful assistant that helps users with the repair of their devices.
                  Ask them if they need help with a repair.
                  If they do, ask them to provide the device name and model."""
    
    if prompt == "repair_guide":
        return (f"List repair steps for the Problem. Use the following context:\n{context}")
    
    if prompt == "repair_helper":
        return (f"Answer the users question about the guide. Use the following context:\n{context}")
   
    
    