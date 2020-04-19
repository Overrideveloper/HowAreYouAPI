from pydantic import BaseModel
from typing import Any

class Response(BaseModel):
    data: Any
    code: int
    message: str
    