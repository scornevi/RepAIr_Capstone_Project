
#%%


#NEW

import gradio as gr
import os
from ui.chat_stream import chatbot_interface #, feedback_positive, feedback_negative
from ui.custom_css import custom_css

def interface_init():
   
    logo_path = "./images/logo.png"

    # Gradio UI
    with gr.Blocks() as app:
        gr.Image(logo_path, elem_id="logo", show_label=False)
        gr.HTML(custom_css())  # Insert custom CSS
        gr.Markdown("### Repair Assistant - Fix smarter with AI")
        gr.Markdown("State your repair topic, select your response style and start chatting.")

        # Input field
        #question = gr.Textbox(label="Your Question", placeholder="What would you like to repair? Please name make, model and problem.")

        # Submit button
        #submit_button = gr.Button("Submit", elem_classes="submit-button")

        # Chat interface & state
        chat_history = gr.State([])
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(placeholder="What would you like to repair? Please name make, model and problem.")
        submit_btn = gr.Button("Submit", elem_classes="submit-button")

        submit_btn.click(chatbot_interface, [chatbot, user_input], chatbot)
        #user_input.submit(chatbot_interface, [chatbot, user_input], chatbot)

        # Response style selection
        response_type = gr.Radio(["Simple Language", "Technical"], label="Answer Style")

        # Connect the start button to chat initialization
        #submit_button.click(fn=start_chat, inputs=[question,response_type], outputs=[chat_history, chatbot, chatbot])

        # "Did the repair work?" label
        gr.Markdown("**Did the repair work?**")

        # Feedback buttons
        with gr.Row(elem_classes="feedback-buttons"):
            thumbs_up = gr.Button("👍 Yes")
            thumbs_down = gr.Button("👎 No")

        # Connect submit button to chatbot function
        #submit_button.click(fn=repair_assistant, inputs=[chat_history, question, response_type], outputs=chatbot)

        # Connect thumbs up to success message (stops chat)
        #thumbs_up.click(fn=feedback_positive, inputs=[chat_history], outputs=chatbot)

        # Connect thumbs down to continue troubleshooting
       # thumbs_down.click(fn=feedback_negative, inputs=[chat_history], outputs=chatbot)
    app.queue().launch()

# %%
