from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPowerPointLoader
import traceback

def load_ppt(temp_file_path: str) -> list[str]:
    """Load PPT and split text into smaller chunks for processing.

    Args:
        temp_file_path (str): Path to the PPT file.

    Returns:
        list[str]: List of text chunks.
    """
    try:
        loader = UnstructuredPowerPointLoader(temp_file_path)
        documents = loader.load()
        
        full_text = "\n\n".join([doc.page_content for doc in documents])

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " "]
        )
        chunks = text_splitter.split_text(full_text)

        return chunks
    except Exception as e:
        print(f"Error loading PPT: {e}")
        traceback.print_exc()
        raise Exception(e)
