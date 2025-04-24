#%%

# Get the interface design and the embedding model
from ui.interface_design import interface_init
from langchain_huggingface import HuggingFaceEmbeddings
import helper_functions.load_embed_model

def main():
    """
    Main entry point of the application.

    - Load the embedding model
    - Intialize the Gradio Repair Assistant interface
    """
    # Load and set the embedding model
    helper_functions.load_embed_model.embedding_model = HuggingFaceEmbeddings(
                                                        model_name='sentence-transformers/all-MiniLM-L6-v2'
                                                        )
    
    # Launch the interface
    interface_init()

if __name__ == "__main__":
    # Ensures main() runs only when the script is executed directly
    main()

# %%
