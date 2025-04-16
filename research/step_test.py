#%%
import gradio as gr

# Your list of instructions
instructions = [
    "🔧 Step 1: Plug in the device and ensure it's powered on.",
    "🧰 Step 2: Check the indicator lights to confirm status.",
    "⚙️ Step 3: Open the settings menu and select 'Reset'.",
    "✅ Step 4: Confirm the action and wait for reboot.",
    "🎉 Done! Setup is complete."
]

# Function to return the next step
def next_instruction(index):
    if index < len(instructions):
        return instructions[index], index + 1
    else:
        return "✅ All steps completed!", index

# Gradio interface
with gr.Blocks() as demo:
    state = gr.State(0)  # Start at step 0
    output = gr.Textbox(label="Instruction", lines=3)
    next_button = gr.Button("Next")

    next_button.click(
        next_instruction,
        inputs=state,
        outputs=[output, state]
    )

demo.launch()
# %%
