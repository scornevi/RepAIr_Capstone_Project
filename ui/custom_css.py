# # Load a custom CSS for Gradio interface

# def custom_css():
#     """
#     Custom CSS for Gradio interface to style buttons, chat container, and background.

#     Returns:
#         str: Custom CSS styles.
#     """
#     custom_css = """
#     <style>
#         .submit-button {
#             background-color: #E69A8D !important; /* Coral Red */
#             color: white !important;
#             border: none;
#             padding: 10px 20px;
#             text-align: center;
#             font-size: 16px;
#             margin: 4px 2px;
#             cursor: pointer;
#             border-radius: 5px;
#         }
#         .submit-button:hover {
#             background-color: #D17F73 !important;
#         }
#         .chat-container {
#             max-height: 500px;
#             overflow-y: auto;
#         }
#         .feedback-buttons {
#             display: flex;
#             gap: 10px;
#             margin-top: 5px;
#         }
#         .gradio-container {
#             background-color: #74BA9C !important;
#         }
#     </style>
#     """
#     return custom_css

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
            height: 100vh;  /* Full viewport height */
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



# def custom_css():
#     """
#     Custom CSS for Gradio interface to style buttons, chat container, and background.

#     Returns:
#         str: Custom CSS styles.
#     """
#     custom_css = """
#     <style>
#         /* General page styling */
#         body, html {
#             margin: 0;
#             padding: 0;
#             height: 90%;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             background-color: #f4f4f4;
#         }

#         /* Gradio container settings */
#         .gradio-container {
#             background-color: #74BA9C !important;
#             width: 100%;
#             max-width: 800px;  /* Adjust max-width for a narrow layout */
#             height: 100%;
#             max-height: 100%;
#             display: flex;
#             flex-direction: column;
#             justify-content: flex-end;
#             border-radius: 10px;
#             box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
#             overflow: hidden;
#         }

#         /* Chat container (message display area) */
#         .chat-container {
#             flex-grow: 1;
#             overflow-y: auto;
#             padding: 10px;
#             max-height: 80%; /* Prevents too much height taken up */
#             margin-bottom: 10px;
#             background-color: #ffffff;
#             border-radius: 10px;
#             box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
#             overflow-wrap: break-word;  /* Ensure long text wraps within the container */
#         }

#         /* Chat input container (below the messages) */
#         .chat-input {
#             display: flex;
#             padding: 10px;
#             border-top: 1px solid #ddd;
#             background-color: #f9f9f9;
#             align-items: center;
#         }

#         .chat-input textarea {
#             flex-grow: 1;
#             padding: 10px;
#             border: 1px solid #ddd;
#             border-radius: 5px;
#             resize: none;
#             height: 40px;
#         }

#         .submit-button {
#             background-color: #E69A8D !important; /* Coral Red */
#             color: white !important;
#             border: none;
#             padding: 10px 20px;
#             text-align: center;
#             font-size: 16px;
#             margin: 4px 2px;
#             cursor: pointer;
#             border-radius: 5px;
#         }

#         .submit-button:hover {
#             background-color: #D17F73 !important;
#         }

#         .feedback-buttons {
#             display: flex;
#             gap: 10px;
#             margin-top: 5px;
#         }

#         /* Chat input and chat container side by side */
#         @media (min-width: 600px) {
#             .gradio-container {
#                 flex-direction: column;
#             }
#             .chat-input {
#                 display: flex;
#                 flex-direction: row;
#                 justify-content: space-between;
#             }
#         }

#         /* Adjust layout for smaller screens (mobile devices) */
#         @media (max-width: 600px) {
#             .gradio-container {
#                 max-width: 100%;
#                 max-height: 100%;
#             }

#             .chat-container {
#                 max-height: 70%; /* Take up less space on smaller screens */
#             }

#             .chat-input textarea {
#                 height: 50px;
#             }
#         }
#     </style>
#     """
#     return custom_css
# def custom_css():
#     """
#     Custom CSS for Gradio interface to style buttons, chat container, and background.
#     Returns:
#         str: Custom CSS styles.
#     """
#     custom_css = """
#     <style>
#         /* Overall page layout */
#         .gradio-container {
#             background-color: #74BA9C !important;
#             display: flex;
#             flex-direction: column;
#             justify-content: flex-start;
#             height: 100vh; /* Full viewport height */
#             width: 100%;  /* Full width */
#             padding: 20px;
#             box-sizing: border-box;
#             overflow: hidden; /* Prevent page scrolling */
#         }

#         /* Container for input and output side by side */
#         .gradio-input-output-container {
#             display: flex;
#             width: 100%;
#             height: 100%; /* Fill the entire page */
#             gap: 20px;
#             flex-grow: 1;
#         }

#         /* Style the input container */
#         .gradio-input-container {
#             flex: 1;  /* Make the input container take up available space */
#             display: flex;
#             flex-direction: column;
#             height: 100%;  /* Full height */
#         }

#         /* Style the output container */
#         .gradio-output-container {
#             flex: 1;  /* Make the output container take up available space */
#             display: flex;
#             flex-direction: column;
#             height: 100%;  /* Full height */
#             overflow-y: auto; /* Enable scrolling for output */
#         }

#         /* Adjust button layout */
#         .gradio-button {
#             width: 100%;
#         }

#         /* Ensure the chat container is scrollable */
#         .chat-container {
#             max-height: calc(100vh - 150px); /* Adjust this value based on layout height */
#             overflow-y: auto; /* Enable scrolling if content exceeds */
#             flex-grow: 1;
#         }

#         /* Remove scrollbars for the entire page */
#         body {
#             margin: 0;
#             padding: 0;
#             overflow: hidden; /* Prevent scrollbars on the entire page */
#         }
#     </style>
#     """
#     return custom_css
