import traceback
from abc import ABC, abstractmethod
from pymilvus import MilvusClient
class CollectionCreateTemplate(ABC):
    def __init__(self,
                client: MilvusClient,
                database_name: str,
                collection_name: str):
        self.client = client
        self.database_name = database_name
        self.collection_name = collection_name
        self.schema = None
        self.index_params  = None
        
        self.process()
        
    def process(self):
        self.create_schema()
        self.create_indexes()
        self.create_collection()
    
    def create_collection(self):
        if self.schema is None:
            raise ValueError("Schema is not created in the function create_schema()")
        
        if self.index_params is None:
            print("Index params has not been initialized, creating database")
            
        if self.database_name not in self.client.list_databases():
            print(f'Creating database {self.database_name}')
            self.client.create_database(self.database_name)
            
        try:
            print('Creating collection')
            self.client.use_database(self.database_name)
            self.client.create_collection(
                collection_name=self.collection_name,
                schema=self.schema,
                index_params=self.index_params
            )
        except Exception as e:
            traceback.print_exc()
            print(f'Error creating collection: {e}')
            
    @abstractmethod
    def create_schema(self):
        pass
    
    @abstractmethod
    def create_indexes(self):
        pass