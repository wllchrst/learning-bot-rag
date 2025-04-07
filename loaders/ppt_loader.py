from langchain.document_loaders import UnstructuredPowerPointLoader

def load_ppt(temp_file_path: str, material_code: str):
    loader = UnstructuredPowerPointLoader(temp_file_path)
    documents = loader.load()

    print(material_code)
    for doc in documents:
        print(doc.page_content)
