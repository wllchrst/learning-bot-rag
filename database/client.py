import traceback
from pymilvus import MilvusClient, utility, connections
from pymilvus.exceptions import MilvusException
from app_decorator import singleton
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
            
    def insert_entity(self, database_name: str, collection_name: str, data: list[dict]):
        try:
            self.client.use_database(database_name)

            self.client.insert(
                collection_name=collection_name,
                data=data
            )
        except Exception as e:
            traceback.print_exc()
            print(f'Insert entity error: {e}')
        finally:
            print("Inserting entity successful")
            return True

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
    
    def search_entities(self,
                    database_name: str,
                    collection_name: str,
                    field: str,
                    query_vector: list[float],
                    output_fields: list[str],
                    metric_type: str = 'COSINE',
                    limit: int = 3
                    ):
        try:
            self.client.use_database(database_name)
            
            result = self.client.search(
                collection_name=collection_name,
                anns_field=field,
                limit=limit,
                search_params={
                    "metric_type": metric_type
                },
                data=[query_vector],
                output_fields=output_fields
            )

            return result[0]
        except Exception as e:
            traceback.print_exc()
            print(f'Error searching entities: {e}')

DatabaseClient()
