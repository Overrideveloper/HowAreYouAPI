from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Response(GenericModel, Generic[T]):
    data: Optional[T]
    code: int
    message: str
    
    
    class Config:
        allow_arbitrary_types = True
