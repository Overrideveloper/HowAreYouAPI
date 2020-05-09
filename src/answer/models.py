from pydantic import BaseModel

class Answer(BaseModel):
    id: int
    answer: str
    question_id: int
    
    class Config:
        schema_extra = {
            "example": {
                "id": 2098,
                "answer": "I am well",
                "question_id": 2145
            }
        }