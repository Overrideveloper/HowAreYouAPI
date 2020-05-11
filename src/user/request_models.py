from pydantic import BaseModel, Field

class SignupLoginUser(BaseModel):
    email: str = Field(..., regex="^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$")
    password: str = Field(..., min_length=6)
    
    class Config:
        schema_extra = {
            "example": {
                "email": "mary@poppins.com",
                "password": "maryispoppinagain"
            }
        }
    
class ChangePassword(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)
    
    class Config:
        schema_extra = {
            "example": {
                "old_password": "maryispoppinagain",
                "new_password": "maryisnotpoppinagain"
            }
        }