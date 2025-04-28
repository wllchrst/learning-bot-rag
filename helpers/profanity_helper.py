from better_profanity import profanity
from app_decorator import singleton
@singleton
class ProfanityHelper:
    def __init__(self):
        profanity.load_censor_words_from_file('bad_words_id.txt')
        
    def check(self, text: str) -> bool:
        return profanity.contains_profanity(text)
