from typing_extensions import TypedDict, List
from models.interfaces.chat_history import ChatHistory

# state = State(
#         answer='',
#         chat_history=[
#                 {
#                     "answer": "",
#                     "chat_id": "chat id",
#                     'question': "What is the rectifier?"
#                 }
#             ],
#         chat_id='',
#         question='What is the function then?',
#         context=''
#     )
class State(TypedDict):
    chat_id: str
    context: List[str]
    question: str
    answer: str
    chat_history: List[ChatHistory]
