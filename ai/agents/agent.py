from abc import ABC, abstractmethod
from scipy import spatial
from models.interfaces.state import State
from models.interfaces.url_data import UrlData
from ai.embeddings import embed_text
from ai.llm import GeminiModel
class Agent(ABC):
    def __init__(self):
        super().__init__()
        self.gemini_model = GeminiModel()
    
    @abstractmethod
    def get_feedback(self, initial_input: State) -> str:
        pass

    def feedback(self, input: str, url_data_list: list[UrlData], top_k=5) -> list[str]:
        input_vector = embed_text(input)
        similarities = []
        
        for data in url_data_list:
            vector = data['vector']
            similarity = spatial.distance.cosine(input_vector, vector)

            similarities.append((data['text'], similarity))
        
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=False)

        results = [item for item, _ in sorted_similarities[:top_k]]
        return results
    
    def generate_answer(self, full_input: str):
        answer = self.gemini_model.answer(full_input)
        return answer
    
    def process_input(self, feedbacks: list[str], role_description: str, question: str):
        information = ''

        for feedback in feedbacks:
            information += f'{feedback}\n\n'
        return f"""
{role_description}

This is the information that have been gathered: 
{information}

This is the question: 
{question}
        """