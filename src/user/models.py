from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    password: str
    
class TokenPayload(BaseModel):
    randomizer: int
    user: str
    expires: float