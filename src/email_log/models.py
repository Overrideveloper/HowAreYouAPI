from pydantic import BaseModel

class EmailLog(BaseModel):
    id: int
    date: str
    count: int