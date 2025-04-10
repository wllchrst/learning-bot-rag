from models.interfaces.state import State
from ai.embeddings import embed_question
from database import DatabaseClient
from helpers import EnvHelper
from ai.llm import GeminiModel
from langgraph.graph import START, StateGraph

class LangchainChat:
    def __init__(self):
        self.dc = DatabaseClient()
        self.eh = EnvHelper()
        self.gm = GeminiModel()
        self.create_graph()
    
    def retrieve(self, state: State):
        print('retrieve')
        question = state['question']
        vector = embed_question(question)

        print(f'question: {question}')
        res = self.dc.search_entities(
            database_name=self.eh.DATABASE_NAME,
            collection_name=self.eh.SESSION_PPT_COLLECTION,
            field="vector",
            query_vector=vector,
            output_fields=['text', 'material_code']
        )

        context: list[str] = [r['entity']['text'] for r in res]
        return {'context': context}

    def generate(self, state: State):
        print('generate')
        full_context = "\n\n".join(state["context"])
        
        prompt = f"""
            Please help me answer the question based on the context given on this chat, but you can also add additional information for the answer, and can you please answer the question without mentioning the context given
            context: {full_context}

            question: {state['question']}
        """
        
        answer = self.gm.answer(prompt)
        return {'answer': answer}
    
    def create_graph(self):
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        self.graph = graph_builder.compile()

    def answer(self, question='What is rectifier?') -> str:
        resp = self.graph.invoke({"question": question})
        print(resp)

        return resp['answer']