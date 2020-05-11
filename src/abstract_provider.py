import abc
from typing import TypeVar, Generic, List, Union, Any
from src.response_models import Response

T = TypeVar('T')

class IProvider(Generic[T], abc.ABC):
    @abc.abstractmethod
    def getAll(self) -> Response[List[T]]:
        pass
    
    @abc.abstractmethod
    def get(self, id: int) -> Union[Response[T], Response]:
        pass
    
    @abc.abstractmethod
    def add(self, req: Any) -> Union[Response[T], Response]:
        pass
    
    @abc.abstractmethod
    def edit(self, id: int, req: Any) -> Union[Response[T], Response]:
        pass
    
    @abc.abstractmethod
    def delete(self, id: int) -> Response:
        pass
    
    
        