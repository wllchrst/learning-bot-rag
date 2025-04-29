"""Handler file that is focused to accept everything related to llm answer question, changin llm settings and other."""
from ai.chat import LangchainChat
from helpers import ProfanityHelper
from models.data.answer_response import AnswerResponse

langchain_chat = LangchainChat()
profanity_helper = ProfanityHelper()

def ask_question(question: str, chat_id: str) -> AnswerResponse:
    result = profanity_helper.check(question)
    if result:
        raise ValueError("Profanity detected in the question., please rephrase it.")
    if chat_id == '':
        chat_id = None
    answer = langchain_chat.answer(question, chat_id)
    return answer
