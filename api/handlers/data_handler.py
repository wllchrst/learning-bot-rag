"""Handler file that is focused on receiving data for the application (User Login, Data for material, session and othe things for indexing)"""
from ai.embeddings import embed_session_ppt
from ai.loaders import load_ppt
from database import DatabaseClient
from helpers import EnvHelper
from dataclasses import asdict

db_client = DatabaseClient()
envhelper = EnvHelper()
def handle_session_ppt(material_code: str, tempfile_path: str):
    contents = load_ppt(tempfile_path)
    session_ppts = embed_session_ppt(contents, material_code)
    
    data = [asdict(session_ppt) for session_ppt in session_ppts]
    success = db_client.insert_entity(
        collection_name=envhelper.SESSION_PPT_COLLECTION,
        database_name=envhelper.DATABASE_NAME,
        data=data
    )

    return success