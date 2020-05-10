from pydantic import BaseModel

class Address(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 3498,
                "name": "John Doe",
                "email": "john@doe.com"
            }
        }