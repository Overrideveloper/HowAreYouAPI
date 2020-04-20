from pydantic import BaseModel

class AddEditQuestion(BaseModel):
    question: str