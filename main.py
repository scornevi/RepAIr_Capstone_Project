#%%

# import checkpoint message
from helper_functions.checkpoint import checkpoint

# get interface design
from ui.interface_design import interface_init
from langchain_huggingface import HuggingFaceEmbeddings
import helper_functions.load_embed_model

def main():
    helper_functions.load_embed_model.embedding_model = HuggingFaceEmbeddings(
                                                        model_name='sentence-transformers/all-MiniLM-L6-v2'
                                                        )
    interface_init()


if __name__ == "__main__":
    main()

checkpoint(__file__)


# %%
