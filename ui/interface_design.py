#%%
import gradio as gr
from chat_logic.chat_stream import feedback_positive, feedback_negative, handle_user_input
from ui.custom_css import custom_css

def interface_init():
    """
    Initialize the Gradio interface for the Repair Assistant chatbot.
    
    This includes setting up the layout, logo, input options, chatbot output, and feedback buttons.
    The UI is divided into two main columns.
    """

    logo_path = "./images/logo.png"

    with gr.Blocks() as app:
        gr.HTML(custom_css())  # Insert custom CSS

        # Define the main layout with two columns
        with gr.Row():
            # Left column: logo, response style options, feedback buttons
            with gr.Column(scale=1, elem_id="gradio-left-container"):
                # Display the logo
                gr.Image(
                    logo_path,
                    elem_id="logo",
                    show_label=False,
                    show_fullscreen_button=False
                )

                # Selection of the response style
                response_type = gr.Radio(
                    ["Simple Language", "Technical", "Homer Simpson Language", "Sarcasm"],
                    label="Answer Style"
                )
                
                # Feedback section (markdown, thumbs up and thumbs down buttons)
                gr.Markdown("🛠️ **Did the repair work?**")
                with gr.Row(elem_classes="feedback-buttons"):
                    thumbs_up = gr.Button("👍 Yes")
                    thumbs_down = gr.Button("👎 No")
                
            # Right column: chat output and user input
            with gr.Column(scale=2, elem_id="gradio-right-container"):
                # Conversation state to manage different dialog stages
                conversation_state = gr.State("interactive_diagnosis")

                # Display chatbot conversation
                chatbot = gr.Chatbot(elem_id="chat-container")
                
                # Input components
                user_input = gr.Textbox(
                    label="Pick an answer style and let the Repair Assistant help you!",
                    placeholder="Your input here",

                    elem_classes="input-textbox"
                )

                # Submit button for sending input
                submit_btn = gr.Button("Submit", elem_classes="submit-button")

                # Define interaction logic for the button and text submit
                submit_btn.click(
                    fn=handle_user_input,
                    inputs=[user_input, chatbot, conversation_state, response_type],
                    outputs=[chatbot, user_input, conversation_state]
                )

                user_input.submit(
                    fn=handle_user_input,
                    inputs=[user_input, chatbot, conversation_state, response_type],
                    outputs=[chatbot, user_input, conversation_state]
                )

        # Feedback logic: thumbs up resets conversation
        thumbs_up.click(
            fn=feedback_positive,
            inputs=[chatbot],
            outputs=[chatbot, user_input, conversation_state]
        )

        # Feedback logic: thumbs down continues with ticket creation
        thumbs_down.click(
            fn=feedback_negative,
            inputs=[chatbot],
            outputs=[chatbot, conversation_state]
        )
    
    app.queue().launch()
