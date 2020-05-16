from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

"""Python 3.6.9 fix:
   - Uncomment the ResponseMetaClass
   - Add `metaclass=ResponseMetaClass` to the Response class args
   - Comment out the nested Config class in Response class
   - Add a __get_validators__ classmethod to arbitrary classes that will be used as type T in this Generic class
"""

# class ResponseMetaClass(type(GenericModel), type(Generic[T])):
#     pass

class Response(GenericModel, Generic[T]):
    data: Optional[T]
    code: int
    message: str
    
    class Config:
        allow_arbitrary_types = True