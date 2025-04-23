def custom_css():
    """
    Custom CSS for Gradio interface to style chat container, buttons, logo, and background.

    Return:
        str: Custom CSS styles embedded in HTML <style> tags.
    """
    custom_css = """
    <style>
        /* Main container for the entire Gradio interface */
        .gradio-container {
            background-color: #74BA9C !important;
            display: flex !important;
            flex-direction: row; /* Make the left and right sections side by side */
            min-height: 100vh;
            padding: 20px;
            box-sizing: border-box;
            width: 100%;
            overflow: visible !important;
        }

        /* Left column: logo, response type radio buttons, feedback sections */
        .gradio-left-container {
            display: flex;
            flex-direction: column;
            width: 40%;  /* Adjust width as needed */
            padding-right: 20px; /* Space between left and right sections */
        }

        /* Right column: chatbot output and input area */
        .gradio-right-container {
            display: flex;
            flex-direction: column;
            flex: 1;
            margin-left: 20px;  /* Space between left and right sections */
        }

        /* Style the logo */
        #logo img {
            width: auto;
            height: 190px;  /* Adjust the height of the logo */
            max-width: 100%;
            margin-bottom: 20px; /* Add margin for spacing between logo and other elements */
        }
        
        #logo {
             background-color: #ffffff !important;
        }

        /* Make the input text box expand to fill available space */
        .input-textbox {
            flex-grow: 1;
            height: 100px;
        }

        /* Submit button style */
        .submit-button {
            background-color: #E69A8D !important;
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

        /* Feedback buttons style */
        .feedback-buttons {
            display: flex;
            gap: 10px;
            margin-top: 5px;
        }

        /* Ensure the full page is responsive */
        body {
            margin: 0;
            padding: 0;
            height: auto;
            overflow-y: auto;
        }

        /* Row layout consistency */
        .gradio-row {
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
        }
    </style>
    """
    return custom_css
