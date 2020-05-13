import abc
from typing import TypeVar, Generic, List, Union, Any
from src.response_models import Response
from sendgrid.helpers.mail import Mail

T = TypeVar('T')

class IDatabase(abc.ABC):
    @abc.abstractmethod
    def get(self, key: str) -> Any:
        pass
    
    @abc.abstractmethod
    def set(self, key: str, data: Any):
        pass
    
    @abc.abstractmethod
    def remove(self, key: str):
        pass

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
    
class IEmailHelper(abc.ABC):
    @abc.abstractmethod
    def createMail(self, recipient: str, subject: str, content: str, html: bool = True) -> Union[Mail, Any]:
        pass
    
    @abc.abstractmethod
    def sendMail(self, mail: Union[Mail, Any]) -> bool:
        pass
        