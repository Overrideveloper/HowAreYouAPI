from pydantic import BaseModel

class LoginResponse(BaseModel):
    email: str
    token: str