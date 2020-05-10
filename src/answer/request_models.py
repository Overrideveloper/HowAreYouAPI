from pydantic import BaseModel

class AddEditAnswer(BaseModel):
    question_id: int
    answer: str
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "I am well",
                "question_id": 2145
            }
        }