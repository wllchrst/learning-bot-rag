"""Handler file that is focused to accept everything related to llm answer question, changin llm settings and other."""
from ai.chat import LangchainChat

langchain_chat = LangchainChat()

def ask_question(question: str) -> str:
    answer = langchain_chat.answer(question)
    return answer