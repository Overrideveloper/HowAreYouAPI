from pydantic import BaseModel

class Address(BaseModel):
    id: int
    name: str
    email: str