from .models import EmailLog
from src.constants import EMAIL_LOG_KEY
from typing import Union, Dict
from src.utils import randomInt
from datetime import date as _date
from src.response_models import Response
from src.abstract_defs import IDatabase

class EmailLogProvider():
    db: IDatabase = None
    
    def __init__(self, db: IDatabase):
        self.db = db

    def addTodayLog(self, count: int):
        logs: Dict[str, dict] = self.db.get(EMAIL_LOG_KEY) or {}
        
        today = _date.today()
        date = "{day}/{month}/{year}".format(day = today.day, month = today.month, year = today.year)

        log = EmailLog(id = randomInt(), date = date, count = count)

        logs[date] = log.dict()
        
        self.db.set(EMAIL_LOG_KEY, logs)

    def getTodaysLog(self) -> Union[Response[EmailLog], Response]:
        logs: Dict[str, dict] = self.db.get(EMAIL_LOG_KEY) or {}
        response: Union[Response[EmailLog], Response] = None
        
        today = _date.today()
        date = "{day}/{month}/{year}".format(day = today.day, month = today.month, year = today.year)

        log = logs.get(date)
        
        if log:
            response = Response[EmailLog](data = EmailLog(**log) , code = 200, message = "Log returned")
        else:
            response = Response(data = None, code = 200, message = "Today's emails not sent yet")
                
        return response