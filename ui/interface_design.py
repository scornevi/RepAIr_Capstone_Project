# interface
import gradio as gr
from ui.chat_stream import chatbot_interface

def interface_init():
    with gr.Blocks() as app:
        gr.Markdown("# 🔧 Fix it! LLaMA3-8B-8192 Chatbot")
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(placeholder="What would you like to repair?")
        submit_btn = gr.Button("Submit")
        
        submit_btn.click(chatbot_interface, [chatbot, user_input], chatbot)
        user_input.submit(chatbot_interface, [chatbot, user_input], chatbot)
    
    app.queue().launch()