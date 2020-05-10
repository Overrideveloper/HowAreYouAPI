from pydantic import BaseModel, Field

class AddEditAddress(BaseModel):
    name: str
    email: str = Field(..., regex="^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@doe.com"
            }
        }