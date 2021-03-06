import redis, json, abc
from typing import Any
from src.constants import REDIS
from src.abstract_defs import IDatabase

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