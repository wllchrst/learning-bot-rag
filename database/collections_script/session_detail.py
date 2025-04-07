from database.collections_script.template import CollectionCreateTemplate
from pymilvus import MilvusClient, DataType
class SessionDetailCollection(CollectionCreateTemplate):
    def __init__(self, client: MilvusClient):
        super().__init__(
            client=client,
            collection_name="session_details",
            database_name="session_data"
        )

    def create_schema(self):
        self.schema = MilvusClient.create_schema(
            auto_id=False,
            enable_dynamic_field=True,
        )
        
        self.schema.add_field(
            field_name="detail_id",
            datatype=DataType.INT64,
            is_primary=True
        )
        
        self.schema.add_field(
            field_name="vector",
            datatype=DataType.FLOAT_VECTOR,
            dim=5
        )
        
        self.schema.add_field(
            field_name="detail_text",
            datatype=DataType.VARCHAR,
            max_length=10000
        )
        
    def create_indexes(self):
        self.index_params = self.client.prepare_index_params()

        self.index_params.add_index(
            field_name="my_id",
            index_type="AUTOINDEX"
        )

        self.index_params.add_index(
            field_name="my_vector", 
            index_type="AUTOINDEX",
            metric_type="COSINE"
        )