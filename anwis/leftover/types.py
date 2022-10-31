from dataclasses import dataclass
from typing import List


@dataclass
class TLeftOverSpecification:
    title: str
    quantity: int


@dataclass
class TLeftOver:
    title: str
    leftovers: List[TLeftOverSpecification]
