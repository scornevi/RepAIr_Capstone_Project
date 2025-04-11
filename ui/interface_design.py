#%%
import gradio as gr
import time
from chat_logic.chat_stream import chatbot_interface, feedback_positive, feedback_negative#, show_follow_up, support_ticket_needed
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
                gr.Image(logo_path, elem_id="logo", show_label=False)

                # Intro text to push the left box lower
                # gr.Markdown("# Pick an answer style and let the Repair Assistant help you!")


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
                chatbot = gr.Chatbot(elem_id="chat-container")
                
                  # Input components
                user_input = gr.Textbox(
                    label="Pick an answer style and let the Repair Assistant help you!",
                    placeholder="Please name device, model and problem.",
                    elem_classes="input-textbox"
                )
                submit_btn = gr.Button("Submit", elem_classes="submit-button")

                

        # Connect buttons and inputs
        submit_btn.click(fn=chatbot_interface, inputs=[chatbot, user_input, response_type], outputs=chatbot)
        user_input.submit(chatbot_interface, [chatbot, user_input, response_type], chatbot)

        # NEW: Support-Follow-up
        #follow_up_input = gr.Textbox(placeholder="Yes or No", label="Support needed?", visible=False)

        # Connect thumbs up to success message (stops chat)
        thumbs_up.click(fn=feedback_positive, inputs=[chat_history], outputs=[chatbot, user_input])

        # NEW (then-Part added)
        # Connect thumbs down to continue troubleshooting
        thumbs_down.click(
            fn=feedback_negative,
            inputs=[chat_history],
            outputs=[chatbot, user_input]
        )#.then(
        #     fn=lambda: gr.update(visible=True),
        #     inputs=None,
        #     outputs=follow_up_input
        # )

        # NEW
        # Query support ticket
        # follow_up_input.submit(
        #     fn=support_ticket_needed,
        #     inputs=[follow_up_input, chatbot],
        #     outputs=[chatbot, follow_up_input]
        # )
        
    app.queue().launch()
