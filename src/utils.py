import random
import string
from src.response_models import Response
from typing import List

def randomInt() -> int:
    return random.randint(1000, 9999)

def randomAlphanumericStr(length: int) -> str:
    return "".join(random.choice(f"{string.digits}{string.ascii_letters}") for i in range(length))

def generate404ResContent(resource: str) -> dict:
    res = { 
        "model": Response,
        "content": {
            "application/json": {
                "example": { "data": None, "code": 404, "message": f"{resource} not found" }       
            }
        }
    }
           
    return res

def generate400ResContent() -> dict:
    res = { 
        "model": Response[List[str]],
        "content": {
            "application/json": {
                "example": { "data": [{ "field": "name", "error": "name is required" }], "code": 400, "message": f"1 validation error for this request: ['name']" }       
            }
        }
    }
           
    return res

def generate403ResContent(message: str) -> dict:
    res = { 
        "model": Response[List[str]],
        "content": {
            "application/json": {
                "example": { "data": None, "code": 403, "message": message }       
            }
        }
    }
           
    return res