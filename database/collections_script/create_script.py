from .session_detail import SessionDetailCollection
from database import DatabaseClient
def create_collections():
    database_client = DatabaseClient()
    SessionDetailCollection(client=database_client.client)