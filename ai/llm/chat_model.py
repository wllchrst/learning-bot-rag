import traceback
from abc import ABC, abstractmethod
class ChatModel(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def answer(self, initial_input: str):
        pass