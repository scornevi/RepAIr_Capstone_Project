# Load a custom CSS for Gradio interface

def custom_css():
    """
    Custom CSS for Gradio interface to style buttons, chat container, and background.

    Returns:
        str: Custom CSS styles.
    """
    custom_css = """
    <style>
        .submit-button {
            background-color: #E69A8D !important; /* Coral Red */
            color: white !important;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .submit-button:hover {
            background-color: #D17F73 !important;
        }
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
        }
        .feedback-buttons {
            display: flex;
            gap: 10px;
            margin-top: 5px;
        }
        .gradio-container {
            background-color: #74BA9C !important;
        }
    </style>
    """
    return custom_css