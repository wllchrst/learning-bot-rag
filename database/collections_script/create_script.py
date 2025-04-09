"""Script for creating all collection"""
from database import DatabaseClient
from database.collections_script import SessionPPTCollection
from helpers import EnvHelper
def create_collections():
    """Script for create all collection that is needed for the application """
    print("create_collections()")
    envhelper = EnvHelper()
    database_client = DatabaseClient()

    SessionPPTCollection(client=database_client.client)

    database_client.list_database()
    database_client.list_collections(database_name=envhelper.DATABASE_NAME)