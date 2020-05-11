from pydantic import BaseModel

class EmailLog(BaseModel):
    id: int
    date: str
    count: int

    class Config:
        schema_extra = {
            "example": {
                "id": 3190,
                "date": "6/5/2020",
                "count": 22
            }
        }