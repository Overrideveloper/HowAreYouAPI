from pydantic import BaseModel

class AddEditAnswer(BaseModel):
    question_id: int
    answer: str