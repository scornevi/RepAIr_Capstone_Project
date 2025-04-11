def custom_css():
    """
    Custom CSS for Gradio interface to style buttons, chat container, and background.

    Returns:
        str: Custom CSS styles.
    """
    custom_css = """
    <style>
        /* Submit button style */
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

        /* Chat container for the right section */
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            flex: 1;
            border: 1px solid #ccc;
            padding: 10px;
            margin-left: 20px;
        }

        /* Feedback buttons layout */
        .feedback-buttons {
            display: flex;
            gap: 10px;
            margin-top: 5px;
        }

        /* Overall container for Gradio interface */
        .gradio-container {
            background-color: #74BA9C !important;
            display: flex !important;
            min-height: 100vh;  /* Full viewport height */
            padding: 20px;
            box-sizing: border-box;
            width: 100%;
            overflow: visible !important;
        }

        /* Left container for input and buttons */
        .gradio-left-container {
            display: flex;
            flex-direction: column;
            width: 40%;  /* Take up 40% of the width */
            height: 100%;  /* Full height */
            padding-right: 20px; /* Space between left and right sections */
        }

        /* Right container for the chat output */
        .gradio-right-container {
            display: flex;
            flex-direction: column;
            flex: 1;
            height: 100%;  /* Full height */
            margin-left: 20px;  /* Space between the input and the chat */
        }

        /* Make the input text box expand to fill available space */
        .input-textbox {
            flex-grow: 1;
            height: 100px;  /* Set a fixed height for the input field */;
            background-color: #f5f5f5 !important; /* Light grey */
        }

        /* Ensure the full page is responsive */
        body {
            margin: 0;
            padding: 0;
            height: auto;
            overflow-y: auto;
        }

        /* Make the Gradio container use full height of the window */
        .gradio-interface {
            height: 100%;
        }

        /* Style the input and output container */
        .gradio-row {
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
        }
                /* Style the logo */
        #logo img {
            width: auto;   /* Auto scale width */
            height: 250px;  /* Set the height for the logo */
            max-width: 100%; /* Ensure the logo doesn't stretch beyond container */
        }


    </style>
    """
    return custom_css