from pydantic import BaseModel

class LoginResponse(BaseModel):
    id: int
    email: str
    token: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": "2097",
                "email": "mary@poppins.com",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyYW5kb21pemVyIjoxODgyLCJ1c2VyIjoiYmFuc293aXNkb21AZ21haWwuY29tIiwiZXhwaXJlcyI6MTU4OTU4MDAwMC4wfQ.3cma3jEirdYAGo4pS_SHIABA2i1Ks-x772jKOyRGbRI",
            }
        }