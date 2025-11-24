from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence


@dataclass
class DataSource:
    name: str
    description: str
    recommended_tools: List[str]
    scraper: Callable[[str], List[Dict[str, str]]]


class Registry:
    def __init__(self, sources: Sequence[DataSource]):
        self.sources = {source.name.lower(): source for source in sources}

    def get(self, name: str) -> DataSource:
        return self.sources[name.lower()]

    def available(self) -> List[str]:
        return list(self.sources.keys())
