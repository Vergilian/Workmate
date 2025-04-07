from abc import ABC, abstractmethod
from typing import Dict


class Report(ABC):
    @abstractmethod
    def generate(self, data: Dict) -> None:
        pass
