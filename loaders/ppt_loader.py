from langchain.document_loaders import UnstructuredPowerPointLoader

def load_ppt(temp_file_path: str, material_code: str):
    """Load PPT and material code, so it can be saved in vector database.

    Args:
        temp_file_path (str): temporary file path that is used for saving the ppt file
        material_code (str): material code for the session detail
    """
    loader = UnstructuredPowerPointLoader(temp_file_path)
    documents = loader.load()

    print(material_code)
    for doc in documents:
        print(doc.page_content)
