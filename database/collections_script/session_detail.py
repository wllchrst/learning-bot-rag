from pymilvus import MilvusClient, DataType
from database.collections_script.template import CollectionCreateTemplate
from helpers import EnvHelper
class SessionDetailCollection(CollectionCreateTemplate):
    def __init__(self, client: MilvusClient):
        envhelper = EnvHelper()
        super().__init__(
            client=client,
            collection_name=envhelper.SESSION_DATA_COLLECTION,
            database_name=envhelper.DATABASE_NAME
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
            field_name="detail_id",
            index_type="AUTOINDEX"
        )

        self.index_params.add_index(
            field_name="vector",
            index_type="AUTOINDEX",
            metric_type="COSINE"
        )
