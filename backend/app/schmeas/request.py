from dataclasses import dataclass

@dataclass
class TextRequest:
    text: str
    style: str
    resolution: str
