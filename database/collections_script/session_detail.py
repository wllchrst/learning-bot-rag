from pymilvus import MilvusClient, DataType
from database.collections_script.template import CollectionCreateTemplate
from helpers import EnvHelper
class SessionPPTCollection(CollectionCreateTemplate):
    def __init__(self, client: MilvusClient):
        envhelper = EnvHelper()
        super().__init__(
            client=client,
            collection_name=envhelper.SESSION_PPT_COLLECTION,
            database_name=envhelper.DATABASE_NAME
        )

    def create_schema(self):
        self.schema = MilvusClient.create_schema(
            auto_id=False,
            enable_dynamic_field=True,
        )

        self.schema.add_field(
            field_name="id",
            datatype=DataType.VARCHAR,
            is_primary=True,
            max_length=36
        )

        self.schema.add_field(
            field_name="vector",
            datatype=DataType.FLOAT_VECTOR,
            dim=768
        )

        self.schema.add_field(
            field_name="text",
            datatype=DataType.VARCHAR,
            max_length=10000
        )
        
        self.schema.add_field(
            field_name="material_code",
            datatype=DataType.VARCHAR,
            max_length=20
        )

    def create_indexes(self):
        self.index_params = self.client.prepare_index_params()

        self.index_params.add_index(
            field_name="id",
            index_type="AUTOINDEX"
        )

        self.index_params.add_index(
            field_name="vector",
            index_type="AUTOINDEX",
            metric_type="COSINE"
        )