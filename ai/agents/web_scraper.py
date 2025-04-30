import requests
import traceback
from googlesearch import search
from bs4 import BeautifulSoup
from ai.agents.agent import Agent
from models.interfaces.state import State
from ai.loaders import load_text_from_web
class WebScraper(Agent):
    def __init__(self):
        super().__init__()
        self.role = "You are an agent that is going to use information gathered from all over the internet and help answer the question"
        
    def get_feedback(self, question: str) -> str:
        links = self.google_search_links(question)
        if len(links) == 0:
            print('No links found')
            return ''
        
        url_data = []
        for link in links:
            if not link or not link.startswith(('http://', 'https://')):
                print(f'Skipping invalid link: {link}')
                continue
            data = self.parse_url(link)
            url_data.extend(data)

        feedbacks = self.feedback(question, url_data)
        input = self.process_input(feedbacks, self.role, question) 
        final_answer = self.generate_answer(input)

        return final_answer

    def google_search_links(self, question: str, number_of_result=2):
        try:
            links = []
            for link in search(question, num_results=number_of_result):
                if link == '':
                    continue
                links.append(link)

            return links
        except Exception as e:
            print(f'Error searching Google: {e}')
            traceback.print_exc()
            return []
    
    def parse_url(self, url: str):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            chunks = load_text_from_web(soup.get_text())
            return chunks
        except Exception as e:
            print(f'Error parsing URL {url}: {e}')
            traceback.print_exc()
            raise