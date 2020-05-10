from pydantic import BaseModel

class AddEditQuestion(BaseModel):
    question: str
    defaultAnswer: str
    
    class Config:
        schema_extra = {
            "example": {
                "question": "Have you eaten?",
                "defaultAnswer": "No, I have not"
            }
        }