from pydantic import BaseModel

class Question(BaseModel):
    id: int
    defaultAnswer: str
    question: str

    class Config:
        schema_extra = {
            "example": {
                "id": 2089,
                "defaultAnswer": "I am well",
                "question": "How are you?"
            }
        }