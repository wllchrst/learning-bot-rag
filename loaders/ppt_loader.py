from langchain.document_loaders import UnstructuredPowerPointLoader

def load_ppt(temp_file_path):
    loader = UnstructuredPowerPointLoader(temp_file_path)
    documents = loader.load()

    for doc in documents:
        print(doc.page_content)
