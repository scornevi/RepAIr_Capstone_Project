
from langchain_community.document_loaders import IFixitLoader
def load_data():
    data = None
    # global data
    if data is None:
        data = IFixitLoader.load_suggestions("iPhone 6", doc_type='guide')
    return data