from typing_extensions import TypedDict, List
class State(TypedDict):
    context: List[str]
    question: str
    answer: str