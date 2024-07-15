from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MatchRecord:
    match_id: str
    championName: str
    winloss: str
