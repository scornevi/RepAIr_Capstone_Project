
# %%

# Version 1: Simple/technical prompt buttons, logo & color integration
# still to fix: color submit button

import gradio as gr
import os

logo_path = os.path.abspath("../../images/branding/logo.png")

# CSS for button color
custom_css = """
<style>
     .submit-button {
        background-color: #E69A8D; /* Button background color coral red */
        color: white; /* Text color */
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px; /* Rounded edges */
    }
     .submit-button:hover {
        background-color: #D17F73; /* Darker coral red when hovering */
    }
     .prompt-button {
        background-color: #A8D5BF !important;
        color: black !important;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        border-radius: 5px;
        margin: 2px;
    }
    .prompt-button:hover {
        background-color: #74BA9C !important;
    }
</style>
"""

def repair_assistant(user_query, response_type):
    prompt = f"Suggested repair steps for: {user_query}\n\n"
    if response_type == "Simple Language":
        prompt += "Please provide a clear and easy-to-understand explanation."
    elif response_type == "Technical":
        prompt += "Provide a detailed technical breakdown of the repair process."
    return prompt

with gr.Blocks() as demo:
    gr.Image(logo_path, elem_id="logo", show_label=False)

    gr.HTML(custom_css)

    gr.Markdown("### Repair Assistant - Fix smarter with AI")
    gr.Markdown("Enter your repair query and get step-by-step instructions.")
    
    # Eingabefeld
    question = gr.Textbox(label="Question", placeholder="What would you like to repair? Please name make, model and problem.")
    
    # Choice of response style
    response_type = gr.Radio(["Simple Language", "Technical"], label="Answer Style")

    # Alternative with colored buttons:
    with gr.Row():
        simple_button = gr.Button("Simple Language", elem_classes=["prompt-button"])
        tech_button = gr.Button("Technical", elem_classes=["prompt-button"])

    # Buttons
    submit_button = gr.Button("Submit", elem_classes="submit-button")
    submit_button.click(fn=repair_assistant, inputs=question, outputs=gr.Textbox(label="RepAIr assistant"))
    

demo.launch()



# %%

# Version 2: Simple/technical prompt buttons, logo & color integration, PLUS: Thumbs up/down
# still to fix: color submit button

import gradio as gr
import os

logo_path = os.path.abspath("../../images/branding/logo.png")

# Custom CSS for styling
custom_css = """
<style>
    .submit-button {
        background-color: #E69A8D; 
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 8px;
        transition: 0.3s;
    }
    .submit-button:hover {
        background-color: #D17F73; 
    }
    .prompt-button {
        background-color: #A8D5BF !important;
        color: black !important;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        border-radius: 5px;
        margin: 2px;
    }
    .prompt-button:hover {
        background-color: #74BA9C !important;
    }
    .response-box {
        background: #F5F5F5; 
        padding: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .feedback-buttons {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }
    .feedback-buttons button {
        font-size: 18px;
        padding: 6px 12px;
        border: none;
        cursor: pointer;
        border-radius: 5px;
        margin: 0 5px;
    }
    .thumbs-up {
        background-color: #4A8A72;
        color: white;
    }
    .thumbs-up:hover {
        background-color: #2E4F4F;
    }
    .thumbs-down {
        background-color: #E69A8D;
        color: white;
    }
    .thumbs-down:hover {
        background-color: #D17F73;
    }
</style>
"""

# Function to return repair instructions
def repair_assistant(user_query, response_type):
    prompt = f"Suggested repair steps for: {user_query}\n\n"
    if response_type == "Simple Language":
        prompt += "Please provide a clear and easy-to-understand explanation."
    elif response_type == "Technical":
        prompt += "Provide a detailed technical breakdown of the repair process."
    return prompt

# Dummy function to handle feedback
def feedback_received(feedback):
    return f"Thank you for your feedback: {feedback}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.HTML(custom_css)

    gr.Image(logo_path, elem_id="logo", show_label=False)
    gr.Markdown("### 🔧 Repair Assistant - Fix smarter with AI")
    gr.Markdown("Enter your repair query and get step-by-step instructions.")

    question = gr.Textbox(label="Question", placeholder="Describe the problem with make & model.")

    response_type = gr.Radio(["Simple Language", "Technical"], label="Answer Style")

    with gr.Row():
        simple_button = gr.Button("Simple Language", elem_classes=["prompt-button"])
        tech_button = gr.Button("Technical", elem_classes=["prompt-button"])

    submit_button = gr.Button("Submit", elem_classes="submit-button")
    response_output = gr.Textbox(label="RepAIr Assistant", elem_classes=["response-box"])

    submit_button.click(fn=repair_assistant, inputs=[question, response_type], outputs=response_output)

    # Feedback Buttons
    with gr.Row(elem_classes=["feedback-buttons"]):
        thumbs_up = gr.Button("👍", elem_classes="thumbs-up")
        thumbs_down = gr.Button("👎", elem_classes="thumbs-down")

    feedback_text = gr.Textbox(label="Feedback Response", visible=False)

    feedback_state = gr.State("")  # Speichert den Feedback-Wert

    thumbs_up.click(fn=feedback_received, inputs=feedback_state, outputs=feedback_text, queue=False)
    thumbs_down.click(fn=feedback_received, inputs=feedback_state, outputs=feedback_text, queue=False)

    # Setze den Feedback-Text
    thumbs_up.click(lambda: "Positive", inputs=[], outputs=feedback_state)
    thumbs_down.click(lambda: "Negative", inputs=[], outputs=feedback_state)

    demo.launch()


# %%

# Version 3: 


import gradio as gr
import os

logo_path = os.path.abspath("../../images/branding/logo.png")

# CSS für das Styling
custom_css = """
<style>
    .submit-button {
        background-color: #E69A8D; /* Coral Red */
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .submit-button:hover {
        background-color: #D17F73;
    }
    .prompt-button {
        background-color: #A8D5BF !important;
        color: black !important;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        border-radius: 5px;
        margin: 2px;
    }
    .prompt-button:hover {
        background-color: #74BA9C !important;
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
</style>
"""

# Funktion zum Starten des Chats
def start_chat(response_type):
    greeting = "Welcome! How can I help you today?" if response_type == "Simple Language" else "Welcome! Please describe your issue in detail."
    return [], gr.update(visible=True), [[None, greeting]]

# Chatbot-Funktion
def repair_assistant(history, user_query, response_type):
    response = f"Suggested repair steps for: {user_query}\n\n"
    if response_type == "Simple Language":
        response += "Please provide a clear and easy-to-understand explanation."
    elif response_type == "Technical":
        response += "Provide a detailed technical breakdown of the repair process."
    
    history.append((user_query, response))  # Chatverlauf speichern
    return history

# Feedback-Funktion
def feedback_received(feedback, history):
    if history:
        history[-1] = (history[-1][0], history[-1][1] + f"\n\nFeedback received: {feedback}")
    return history

# Gradio UI
with gr.Blocks() as demo:
    gr.Image(logo_path, elem_id="logo", show_label=False)

    gr.HTML(custom_css)  # CSS einfügen

    gr.Markdown("### Repair Assistant - Fix smarter with AI")
    gr.Markdown("Select your response style and start chatting.")

    # Auswahl für Antwortstil
    response_type = gr.Radio(["Simple Language", "Technical"], label="Answer Style")

    # Start-Button
    start_button = gr.Button("Start Chat", elem_classes="submit-button")

    # Chat-Interface & State
    chat_history = gr.State([])
    chatbot = gr.Chatbot(label="Repair Assistant", elem_classes="chat-container", visible=False)

    # Verbindung des Start-Buttons mit der Chat-Initialisierung
    start_button.click(fn=start_chat, inputs=[response_type], outputs=[chat_history, chatbot, chatbot])

    # Eingabefeld
    question = gr.Textbox(label="Your Question", placeholder="Describe your repair problem...")

    # Senden-Button
    submit_button = gr.Button("Submit", elem_id="custom-submit-btn")

    # Feedback-Buttons
    with gr.Row(elem_classes="feedback-buttons"):
        thumbs_up = gr.Button("👍")
        thumbs_down = gr.Button("👎")

    # Verbindung des Submit-Buttons mit der Chat-Funktion
    submit_button.click(fn=repair_assistant, inputs=[chat_history, question, response_type], outputs=chatbot)
    
    # Verbindung der Feedback-Buttons mit der Feedback-Funktion
    thumbs_up.click(fn=feedback_received, inputs=[gr.State("Positive"), chat_history], outputs=chatbot)
    thumbs_down.click(fn=feedback_received, inputs=[gr.State("Negative"), chat_history], outputs=chatbot)

demo.launch()

# %%

# Version 3: Did the repair work? Question at the end. Thumbs up stops chat.

import gradio as gr
import os

logo_path = os.path.abspath("../../images/branding/logo.png")

# CSS for styling
custom_css = """
<style>
    .submit-button {
        background-color: #E69A8D; /* Coral Red */
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .submit-button:hover {
        background-color: #D17F73;
    }
    .prompt-button {
        background-color: #A8D5BF !important;
        color: black !important;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        border-radius: 5px;
        margin: 2px;
    }
    .prompt-button:hover {
        background-color: #74BA9C !important;
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
</style>
"""

# Function to start the chat
def start_chat(response_type):
    greeting = "Welcome! How can I help you today?" if response_type == "Simple Language" else "Welcome! Please describe your issue in detail."
    return [], gr.update(visible=True), [[None, greeting]]

# Chatbot function
def repair_assistant(history, user_query, response_type):
    response = f"Suggested repair steps for: {user_query}\n\n"
    if response_type == "Simple Language":
        response += "Please provide a clear and easy-to-understand explanation."
    elif response_type == "Technical":
        response += "Provide a detailed technical breakdown of the repair process."
    
    history.append((user_query, response))  # Append to chat history
    return history

# Feedback function for thumbs up (chat ends with success message)
def feedback_positive(history):
    history.append((None, "🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask."))
    return history

# Feedback function for thumbs down (chat continues)
def feedback_negative(history):
    history.append((None, "I'm sorry to hear that. Could you describe the issue further? Maybe we can find another solution."))
    return history

# Gradio UI
with gr.Blocks() as demo:
    gr.Image(logo_path, elem_id="logo", show_label=False)

    gr.HTML(custom_css)  # Insert custom CSS

    gr.Markdown("### Repair Assistant - Fix smarter with AI")
    gr.Markdown("Select your response style and start chatting.")

    # Response style selection
    response_type = gr.Radio(["Simple Language", "Technical"], label="Answer Style")

    # Start button
    start_button = gr.Button("Start Chat", elem_classes="submit-button")

    # Chat interface & state
    chat_history = gr.State([])
    chatbot = gr.Chatbot(label="Repair Assistant", elem_classes="chat-container", visible=False)

    # Connect the start button to chat initialization
    start_button.click(fn=start_chat, inputs=[response_type], outputs=[chat_history, chatbot, chatbot])

    # Input field
    question = gr.Textbox(label="Your Question", placeholder="Describe your repair problem...")

    # Submit button
    submit_button = gr.Button("Submit", elem_id="custom-submit-btn")

    # "Did the repair work?" label
    gr.Markdown("**Did the repair work?**")

    # Feedback buttons
    with gr.Row(elem_classes="feedback-buttons"):
        thumbs_up = gr.Button("👍 Yes")
        thumbs_down = gr.Button("👎 No")

    # Connect submit button to chatbot function
    submit_button.click(fn=repair_assistant, inputs=[chat_history, question, response_type], outputs=chatbot)
    
    # Connect thumbs up to success message (stops chat)
    thumbs_up.click(fn=feedback_positive, inputs=[chat_history], outputs=chatbot)

    # Connect thumbs down to continue troubleshooting
    thumbs_down.click(fn=feedback_negative, inputs=[chat_history], outputs=chatbot)

demo.launch()

# %%

# Version 4: Merge version

import gradio as gr
import os

logo_path = os.path.abspath("../../images/branding/logo.png")

# CSS for styling
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
</style>
"""

# Function to start the chat
def start_chat(response_type):
    greeting = "Welcome! How can I help you today?" if response_type == "Simple Language" else "Welcome! Please describe your issue in detail."
    return [], gr.update(visible=True), [[None, greeting]]

# Chatbot function
def repair_assistant(history, user_query, response_type):
    response = f"Suggested repair steps for: {user_query}\n\n"
    if response_type == "Simple Language":
        response += "Please provide a clear and easy-to-understand explanation."
    elif response_type == "Technical":
        response += "Provide a detailed technical breakdown of the repair process."
    
    history.append((user_query, response))  # Append to chat history
    return history

# Feedback function for thumbs up (chat ends with success message)
def feedback_positive(history):
    history.append((None, "🎉 Great! We're happy to hear that your repair was successful! If you need help in the future, feel free to ask."))
    return history

# Feedback function for thumbs down (chat continues)
def feedback_negative(history):
    history.append((None, "I'm sorry to hear that. Could you describe the issue further? Maybe we can find another solution."))
    return history

# Gradio UI
with gr.Blocks() as demo:
    gr.Image(logo_path, elem_id="logo", show_label=False)
    gr.HTML(custom_css)  # Insert custom CSS
    gr.Markdown("### Repair Assistant - Fix smarter with AI")
    gr.Markdown("State your repair topic, select your response style and start chatting.")

    # Input field
    question = gr.Textbox(label="Your Question", placeholder="What would you like to repair? Please name make, model and problem.")

    # Response style selection
    response_type = gr.Radio(["Simple Language", "Technical"], label="Answer Style")

    # Submit button
    submit_button = gr.Button("Submit", elem_classes="submit-button")

    # Chat interface & state
    chat_history = gr.State([])
    chatbot = gr.Chatbot(label="Repair Assistant", elem_classes="chat-container", visible=False)

    # Connect the start button to chat initialization
    submit_button.click(fn=start_chat, inputs=[question,response_type], outputs=[chat_history, chatbot, chatbot])

    # "Did the repair work?" label
    gr.Markdown("**Did the repair work?**")

    # Feedback buttons
    with gr.Row(elem_classes="feedback-buttons"):
        thumbs_up = gr.Button("👍 Yes")
        thumbs_down = gr.Button("👎 No")

    # Connect submit button to chatbot function
    submit_button.click(fn=repair_assistant, inputs=[chat_history, question, response_type], outputs=chatbot)
    
    # Connect thumbs up to success message (stops chat)
    thumbs_up.click(fn=feedback_positive, inputs=[chat_history], outputs=chatbot)

    # Connect thumbs down to continue troubleshooting
    thumbs_down.click(fn=feedback_negative, inputs=[chat_history], outputs=chatbot)

demo.launch()
# %%
