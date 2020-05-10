from pydantic import BaseModel

class LoginResponse(BaseModel):
    email: str
    token: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john@doe.com",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyYW5kb21pemVyIjoxODgyLCJ1c2VyIjoiYmFuc293aXNkb21AZ21haWwuY29tIiwiZXhwaXJlcyI6MTU4OTU4MDAwMC4wfQ.3cma3jEirdYAGo4pS_SHIABA2i1Ks-x772jKOyRGbRI",
            }
        }