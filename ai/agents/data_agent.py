from ai.agents import Agent
from models.interfaces.state import State
from ai.embeddings import embed_text
from helpers import EnvHelper
from database import DatabaseClient
from database.client import DatabaseClient
class DataAgent(Agent):
    def __init__(self):
        super().__init__()
        self.database_client = DatabaseClient()
        self.env_helper = EnvHelper()
        self.role_desc = 'You are an agent that is going to receive information from material that is factual and came from University Lectures, Material Session data and other factual information'
    
    def get_feedback(self, initial_input: State) -> str:
        question = initial_input['question']
        question_vector = embed_text(question)

        search_result = self.database_client.search_entities(
            database_name=self.env_helper.DATABASE_NAME,
            collection_name=self.env_helper.SESSION_PPT_COLLECTION,
            field="vector",
            query_vector=question_vector,
            output_fields=['text', 'material_code']
        )

        information_list = [data['entity']['text'] for data in search_result]

        final_input = self.process_input(
            information_list=information_list,
            role_description=self.role_desc,
            question=question
        )

        print(final_input)