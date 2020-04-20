import redis
import json
from typing import Any
from src.constants import REDIS

db = redis.StrictRedis(host = REDIS["HOST"], port=REDIS["PORT"])

def get(key: str):
    data = db.get(key)
    
    return json.loads(data) if data is not None else data

def set(key: str, data: Any):
    db.set(key, json.dumps(data))
    
def remove(key: str):
    db.delete(key)