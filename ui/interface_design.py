#%%
import gradio as gr
from chat_logic.chat_stream import chatbot_interface, feedback_positive, feedback_negative, handle_user_input
from ui.custom_css import custom_css

def interface_init():
    """
    Initialize the Gradio interface for the Repair Assistant chatbot.
    """

    logo_path = "./images/logo.png"

    # Gradio UI
    with gr.Blocks() as app:
        gr.HTML(custom_css())  # Insert custom CSS

        # Create a row for the layout
        with gr.Row():
            # Left container for the logo, input, and buttons
            with gr.Column(scale=1, elem_id="gradio-left-container"):
                # Logo
                gr.Image(logo_path, elem_id="logo", show_label=False, show_fullscreen_button=False)

                response_type = gr.Radio(
                    ["Simple Language", "Technical", "Homer Simpson Language", "Sarcasm"],
                    label="Answer Style"
                )
                
                # Feedback section (thumbs up and thumbs down buttons, and markdown)
                gr.Markdown("🛠️ **Did the repair work?**")
                with gr.Row(elem_classes="feedback-buttons"):
                    thumbs_up = gr.Button("👍 Yes")
                    thumbs_down = gr.Button("👎 No")
                
            # Right container for the chat output and feedback buttons
            with gr.Column(scale=2, elem_id="gradio-right-container"):
                # Chat history output
                chat_history = gr.State([])  # For maintaining the chat state
                conversation_state = gr.State("interactive_diagnosis") # For awaiting the users response if support ticket is needed

                chatbot = gr.Chatbot(elem_id="chat-container")
                
                # Input components
                user_input = gr.Textbox(
                    label="Pick an answer style and let the Repair Assistant help you!",
                    placeholder="Your input here",

                    elem_classes="input-textbox"
                )
                submit_btn = gr.Button("Submit", elem_classes="submit-button")

                # NEW:
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

        # Connect thumbs up to success message (stops chat)
        thumbs_up.click(
            fn=feedback_positive,
            inputs=[chatbot],
            outputs=[chatbot, user_input, conversation_state]
        )

        # NEW: Connect thumbs down
        thumbs_down.click(
            fn=feedback_negative,
            inputs=[chatbot],
            outputs=[chatbot, conversation_state]
        )
    
    app.queue().launch()
