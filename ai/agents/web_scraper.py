import requests
from googlesearch import search
from bs4 import BeautifulSoup
from ai.agents.agent import Agent
from models.interfaces.state import State
from ai.loaders import load_text_from_web
class WebScraper(Agent):
    def __init__(self):
        super().__init__()
        self.role = "You are an agent that is going to use information gathered from all over the internet and help answer the question"
        
    def get_feedback(self, initial_input: State) -> str:
        question = initial_input['question']
        links = self.google_search_links(question)
        
        url_data = []
        for link in links:
            data = self.parse_url(link)
            url_data.extend(data)

        feedbacks = self.feedback(question, url_data)
        input = self.process_input(feedbacks, self.role, question) 
        final_answer = self.generate_answer(input)

        return final_answer

    def google_search_links(self, question: str, number_of_result=2):
        links = []
        for link in search(question, num_results=number_of_result):
            if link == '':
                continue
            links.append(link)

        return links
    
    def parse_url(self, url: str):
        print(f'url: {url}')
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        chunks = load_text_from_web(soup.get_text())
        return chunks