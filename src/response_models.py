from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Optional
from pydantic import Field

T = TypeVar('T')

class Response(GenericModel, Generic[T]):
    data: Optional[T]
    code: int
    message: str
    
    
    class Config:
        allow_arbitrary_types = True
