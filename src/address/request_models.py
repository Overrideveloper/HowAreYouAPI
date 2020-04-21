from pydantic import BaseModel

class AddEditAddress(BaseModel):
    name: str
    email: str