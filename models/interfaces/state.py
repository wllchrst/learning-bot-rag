from typing_extensions import TypedDict, List
from models.interfaces.chat_history import ChatHistory

class State(TypedDict):
    chat_id: str
    context: List[str]
    question: str
    answer: str
    chat_history: List[ChatHistory]
