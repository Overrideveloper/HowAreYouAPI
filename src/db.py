import redis, json, abc
from typing import Any
from src.constants import REDIS

class IDatabase(abc.ABC):
    @abc.abstractmethod
    def get(self, key: str) -> Any:
        pass
    
    @abc.abstractmethod
    def set(self, key: str, data: Any):
        pass
    
    @abc.abstractmethod
    def remove(self, key: str):
        pass


class Database(IDatabase):
    db: redis.Redis = None

    def __init__(self):
        self.db = redis.StrictRedis(host = REDIS["HOST"], port=REDIS["PORT"])
    
    def get(self, key: str) -> Any:
        data = self.db.get(key)

        return json.loads(data) if data is not None else data

    def set(self, key: str, data: Any):
        self.db.set(key, json.dumps(data))
        
    def remove(self, key: str):
        self.db.delete(key)