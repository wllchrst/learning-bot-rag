import traceback
from pymilvus import MilvusClient, utility, connections
from pymilvus.exceptions import MilvusException
from app_decorator import singleton
from database.collections_script.create_script import create_collections
@singleton
class DatabaseClient:
    def __init__(self, uri='http://localhost:19530'):
        self.uri = uri
        self.connect()

    def connect(self):
        try:
            connections.connect(alias="default", uri=self.uri, token="root:Milvus")
            self.client = MilvusClient(uri=self.uri, token="root:Milvus")

            print(f'Connected to database with version: {utility.get_server_version()}')
        except Exception as e:
            traceback.print_exc()
            print(f'Connecting to database server error: {e}')
            
    def insert_entity(self, collection_name: str, data: dict):
        try:
            self.client.insert(
                collection_name=collection_name,
                data=data
            )
        except Exception as e:
            traceback.print_exc()
            print(f'Connecting to database server error: {e}')

    def create_database(self, database_name: str):
        try:
            print('creating database')
            self.client.create_database(db_name=database_name)
        except MilvusException as e:
            traceback.print_exc()
            print(f'Creating database error: {e}')

    def list_database(self):
        try:
            dbs = self.client.list_databases()
            print(f'databases: {dbs}')
        except MilvusException as e:
            traceback.print_exc()
            print(f'Listing database error: {e}')
        
    def use_database(self, database_name: str):
        try:
            self.client.use_database(db_name=database_name)
        except MilvusException as e:
            traceback.print_exc()
            print(f'Switching database error: {e}')
            
    def delete_database(self, database_name: str):
        try:
            if database_name in self.client.list_databases():
                self.client.drop_database(database_name)
        except Exception as e:
            traceback.print_exc()
            print(f'Deleting database: {e}')
    
    def list_collections(self, database_name: str):
        try:
            self.client.use_database(database_name)
            collections = self.client.list_collections()
            print(f'Collections in the database: {collections}')
        except Exception as e:
            traceback.print_exc()
            print(f'Error listing collection: {e}')

DatabaseClient()
