from pydantic import BaseModel, Field

class AddEditQuestion(BaseModel):
    question: str = Field(..., min_length=1)
    defaultAnswer: str = Field(..., min_length=1)
    
    class Config:
        schema_extra = {
            "example": {
                "question": "Have you eaten?",
                "defaultAnswer": "No, I have not"
            }
        }