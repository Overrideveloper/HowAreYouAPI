from src.abstract_defs import IDatabase
from typing import Dict, Any, Union

class DatabaseMock(IDatabase):
    data: Dict[str, str] = {}

    def __init__(self, data: Dict[str, str] = {}):
        self.data = data
    
    def get(self, key: str) -> Union[Any, None]:
        return self.data.get(key)
    
    def set(self, key: str, data: Any):
        self.data[key] = data
    
    def remove(self, key: str):
        if self.data.get(key):
            del self.data[key]