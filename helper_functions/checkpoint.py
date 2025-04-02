import os

def checkpoint(path):
    """Prints a message indicating the successful execution of a script.
    It will give you the script name where this function is calles by default.
    Alternatively, you can set a string to display a custom message."""
    
    script_name = os.path.basename(path)  # Extract just the filename
    
    print("-" * 30)
    print(f"{script_name} successfully executed!")
    print("-" * 30)
