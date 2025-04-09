from dataclasses import dataclass
@dataclass
class SessionPPTData:
    id: int
    vector: list[float]
    material_code: str
    text: str