import traceback
from ai.llm import GeminiModel
from langgraph.graph import START, StateGraph
from typing import Dict
from helpers import ULIDHelper
from models.interfaces.state import State
from models.interfaces.chat_history import ChatHistory
from models.data.answer_response import AnswerResponse
from database import DatabaseClient
from helpers import EnvHelper
from ai.agents import WebScraper, DataAgent

class LangchainChat:
    """
    LangchainChat handles the interaction between a user and an LLM-powered chatbot,
    including question embedding, context retrieval, prompt generation, and managing
    in-memory chat history.

    Attributes:
        dc (DatabaseClient): Interface for database search operations.
        eh (EnvHelper): Loads environment variables and configurations.
        gm (GeminiModel): Large language model used to generate responses.
        chat_history (Dict[str, list[ChatHistory]]): In-memory store for chat sessions.
        graph (StateGraph): LangGraph pipeline for chaining retrieval and generation.
    """

    def __init__(self):
        """
        Initializes the LangchainChat instance by setting up dependencies and
        compiling the LangGraph pipeline.
        """
        self.dc = DatabaseClient()
        self.eh = EnvHelper()
        self.gm = GeminiModel()
        self.web_scraper = WebScraper()
        self.data_agent = DataAgent()
        self.chat_history: Dict[str, list[ChatHistory]] = {}
        self.create_graph()

    def retrieve(self, state: State):
        """
        Retrieves contextual documents based on the embedded question vector.

        Args:
            state (State): Contains the user's question and chat ID.

        Returns:
            dict: Contextual text list and existing chat history for the session.
        """
        web_feedback = self.web_scraper.get_feedback(state)
        data_feedback = self.data_agent.get_feedback(state)
        context = [web_feedback, data_feedback]

        chat_history = None if state['chat_id'] not in self.chat_history\
            else self.chat_history[state['chat_id']]

        return {'context': context, 'chat_history': chat_history}

    def generate(self, state: State):
        """
        Generates a response using the LLM based on context and prior chat history.

        Args:
            state (State): Contains context, previous chat history, and the current question.

        Returns:
            dict: Generated answer.
        """
        full_context = "\n\n".join(state["context"])
        formatted_chat_history = ''
        chat_history = state['chat_history']
        if chat_history is not None:
            for chat in chat_history:
                print(f'chat: {chat}')
                formatted_chat_history += f"User: {chat['question']}\nAssistant: {chat['answer']}\n\n"

        prompt = f"""
Please help me answer the question based on the context given on this chat, but you can also add additional information for the answer, and can you please answer the question without mentioning the context given
context: {full_context}

chat_history:
{formatted_chat_history}

question: {state['question']}
        """

        print(prompt)
        answer = self.gm.answer(prompt)
        return {'answer': answer}

    def create_graph(self):
        """
        Builds and compiles the LangGraph pipeline which defines the flow from retrieval to generation.
        """
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        self.graph = graph_builder.compile()

    def save_chat(self, chat_id: str, question: str, answer: str):
        """
        Saves a single question-answer pair into the in-memory chat history.

        Args:
            chat_id (str): Unique ID for the chat session.
            question (str): User's question.
            answer (str): Assistant's response.

        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            chat = ChatHistory(chat_id=chat_id, question=question, answer=answer)

            if chat_id not in self.chat_history:
                self.chat_history[chat_id] = []

            self.chat_history[chat_id].append(chat)

            return True
        except Exception as e:
            traceback.print_exc()
            print(f'Error saving chat: {e}')
            return False

    def answer(self, question='What is rectifier?', chat_id: str = None) -> AnswerResponse:
        """
        Processes a user question by invoking the LangGraph pipeline, generates an answer,
        and saves it to chat history.

        Args:
            question (str): User's input question.
            chat_id (str, optional): Existing chat session ID. If None, a new one is generated.

        Returns:
            AnswerResponse: Contains the chat ID and generated answer.
        """
        try:
            if chat_id is None:
                chat_id = ULIDHelper().generate_ulid()

            resp = self.graph.invoke({"question": question, "chat_id": chat_id})

            self.save_chat(chat_id, question, resp['answer'])

            return AnswerResponse(
                chat_id=chat_id,
                answer=resp['answer']
            )
        except Exception as e:
            print(e)
            traceback.print_exc()
