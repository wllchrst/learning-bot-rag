from app_decorator.singleton import singleton
from ulid import ULID
@singleton
class ULIDHelper:
    def __init__(self):
        pass
    
    def generate_ulid(self):
        ulid = ULID()
        return str(ulid)