import random
from src.response_models import Response
from typing import List

def randomInt() -> int:
    return random.randint(1000, 9999)

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
                "example": { "data": ["field required"], "code": 400, "message": f"1 validation error for this request: ['field']" }       
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