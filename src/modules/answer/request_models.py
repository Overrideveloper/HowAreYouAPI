from pydantic import BaseModel, Field

class AddEditAnswer(BaseModel):
    question_id: int = Field(..., gt=0)
    answer: str = Field(..., min_length=1)
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "I am well",
                "question_id": 2145
            }
        }