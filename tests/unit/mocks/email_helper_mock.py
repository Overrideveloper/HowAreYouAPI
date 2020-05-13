from src.abstract_defs import IEmailHelper
from typing import Any

class EmailHelperMock(IEmailHelper):
    def __init__(self):
        pass
    
    def createMail(self, recipient: str, subject: str, content: str, html: bool = True) -> dict:
        return { }
    
    def sendMail(self, mail: Any) -> bool:
        return True