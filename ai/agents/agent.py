from abc import ABC, abstractmethod
from scipy import spatial
from models.interfaces.state import State
from models.interfaces.url_data import UrlData
from ai.embeddings import embed_text
from ai.llm import GeminiModel
from models.interfaces.chat_history import ChatHistory
class Agent(ABC):
    def __init__(self):
        super().__init__()
        self.gemini_model = GeminiModel()
    
    @abstractmethod
    def get_feedback(self, question: str) -> str:
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
    
    def conclude_question_by_chat_history(self, state: State):
        if 'chat_history' not in state:
            return state['question']
        if state['chat_history'] == None or len(state['chat_history']) == 0:
            return state['question']

        questions = [history['question'] for history in state['chat_history']]
        formatted_history = 'Chat History:\n'
        
        for q in questions:
            formatted_history += f'- {q}\n'
        
        formatted_history += f'\nUser Last Question: {state['question']}'

        prompt = f'''
Can you help me conclude the question based on the context of chat history, just give me the end result

{formatted_history}
        '''

        print(f'Promopt CONCLUDE: {prompt}')

        answer = self.gemini_model\
            .answer(prompt)
        
        return answer

    def process_input(self, information_list: list[str], role_description: str, question: str):
        full_information = ''

        for info in information_list:
            full_information += f'{info}\n\n'
        return f"""
{role_description}

This is the information that have been gathered: 
{full_information}

This is the question: 
{question}
        """