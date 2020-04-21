from pydantic import BaseModel

class Answer(BaseModel):
    id: int
    answer: str
    question_id: int