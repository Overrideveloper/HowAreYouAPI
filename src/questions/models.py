from pydantic import BaseModel

class Question(BaseModel):
    id: int
    defaultAnswer: str
    question: str