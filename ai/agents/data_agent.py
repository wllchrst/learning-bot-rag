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
    
    def get_feedback(self, question: str) -> str:
        question_vector = embed_text(question)

        search_results = self.database_client.search_entities(
            database_name=self.env_helper.DATABASE_NAME,
            collection_name=self.env_helper.SESSION_PPT_COLLECTION,
            field="vector",
            query_vector=question_vector,
            output_fields=['text', 'material_code']
        )

        search_results = self.validate_information_relevance(search_results)

        if(len(search_results) == 0) :
            print("There is no enough relevant document in vector database")
            return ''
        
        information_list = [data['entity']['text'] for data in search_results]

        final_input = self.process_input(
            information_list=information_list,
            role_description=self.role_desc,
            question=question
        )

        return self.generate_answer(final_input)

    def validate_information_relevance(self, search_results: list[dict], distance_treshold=0.3):
        filtered_results = []
        
        for result in search_results:
            distance = result['distance']
            if distance < distance_treshold:
                continue
            filtered_results.append(result)
        
        return filtered_results