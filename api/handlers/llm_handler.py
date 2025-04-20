"""Handler file that is focused to accept everything related to llm answer question, changin llm settings and other."""
from ai.chat import LangchainChat

langchain_chat = LangchainChat()

def ask_question(question: str, chat_id: str) -> str:
    if chat_id == '':
        chat_id = None
    answer = langchain_chat.answer(question, chat_id)
    return answer
