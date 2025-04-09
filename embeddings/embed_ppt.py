from langchain_huggingface import HuggingFaceEmbeddings
from models.data.session_ppt_data import SessionPPTData
from helpers import ULIDHelper

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

def embed_session_ppt(texts: list[str], material_code: str) -> list[SessionPPTData]:
    vectors = hf.embed_documents(texts)
    result: list[SessionPPTData] = []
    
    for vector, text in zip(vectors, texts):
        print(f'vector length: {len(vector)}')
        result.append(
            SessionPPTData(
                id=ULIDHelper().generate_ulid(),
                material_code=material_code,
                text=text,
                vector=vector
            )
        )
        
    return result