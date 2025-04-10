
#%%

import gradio as gr
from chat_logic.chat_stream import chatbot_interface, feedback_positive, feedback_negative, support_ticket_needed
from ui.custom_css import custom_css

def interface_init():
    """
    Initialize the Gradio interface for the Repair Assistant chatbot.

    """
   
    logo_path = "./images/logo.png"

    # Gradio UI
    with gr.Blocks() as app:
        gr.Image(logo_path, elem_id="logo", show_label=False)
        gr.HTML(custom_css())  # Insert custom CSS
        gr.Markdown("### Repair Assistant - Fix smarter with AI")
        gr.Markdown("State your repair topic, select your response style and start chatting.")

        # Chat interface & state
        chat_history = gr.State([])
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(placeholder="What would you like to repair? Please name make, model and problem.")
        response_type = gr.Radio(["Simple Language", "Technical", "Homer Simpson Language", "Sarcasm"], label="Answer Style")
        submit_btn = gr.Button("Submit", elem_classes="submit-button")

        submit_btn.click(fn=chatbot_interface, inputs=[chatbot, user_input, response_type], outputs=chatbot)
        user_input.submit(chatbot_interface, [chatbot, user_input, response_type], chatbot)

        # "Did the repair work?" label
        gr.Markdown("**Did the repair work?**")

        # NEW: Support-Follow-up
        follow_up_input = gr.Textbox(placeholder="Yes or No", label="Support needed?", visible=False)

        # Feedback buttons (not functional yet)
        with gr.Row(elem_classes="feedback-buttons"):
            thumbs_up = gr.Button("👍 Yes")
            thumbs_down = gr.Button("👎 No")

        # Connect thumbs up to success message (stops chat)
        thumbs_up.click(fn=feedback_positive, inputs=[chat_history], outputs=[chatbot, user_input]) # NEU: user_input added

        # NEW (then-Part added)
        # Connect thumbs down to continue troubleshooting
        thumbs_down.click(
            fn=feedback_negative,
            inputs=[chat_history],
            outputs=chatbot
        ).then(
            fn=lambda: gr.update(visible=True),
            inputs=None,
            outputs=follow_up_input
        )

        # NEW
        # Query support ticket
        follow_up_input.submit(
            fn=support_ticket_needed,
            inputs=[follow_up_input, chatbot],
            outputs=[chatbot, follow_up_input]
        )
        
    app.queue().launch()

