from typing_extensions import TypedDict
class ChatHistory(TypedDict):
    chat_id: str
    question: str
    answer: str
