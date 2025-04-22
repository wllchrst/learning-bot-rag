from langchain.text_splitter import RecursiveCharacterTextSplitter
from models.interfaces.url_data import UrlData
from ai.embeddings import embed_text
import re

def clean_text(text) -> str:
    """
    Cleans the input text by replacing unwanted characters with spaces.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    text = re.sub(r'[\t\n]+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def load_text_from_web(input: str) -> list[UrlData]:
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=50,
            separators=["\n\n", "\n", " "]
        )
        chunks = text_splitter.split_text(input)

        final_result: list[UrlData] = []
        
        for c in chunks:
            processed = clean_text(c)
            vector = embed_text(processed)

            final_result.append(UrlData(
                text=processed,
                vector=vector
            ))

        return final_result
    except Exception as e:
        print(f"Error loading PPT: {e}")
        raise Exception(e)
 