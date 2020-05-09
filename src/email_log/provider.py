from src.email_log.models import EmailLog
from src.constants import EMAIL_LOG_KEY
from typing import List
from src.utils import randomInt
from datetime import date as _date
from src.response_models import Response
from src.email_log.models import EmailLog
import src.db as db

def addTodayLog(count: int):
    logs: List[dict] = db.get(EMAIL_LOG_KEY) or []
    
    today = _date.today()
    date = "{day}/{month}/{year}".format(day = today.day, month = today.month, year = today.year)

    log = EmailLog(id = randomInt(), date = date, count = count)
    
    logs.append(log.dict())
    db.set(EMAIL_LOG_KEY, logs)

def getTodaysLog() -> Response[EmailLog]:
    logs: List[dict] = db.get(EMAIL_LOG_KEY) or []
    response: Response[EmailLog] = None
    log: dict = None
    
    today = _date.today()
    date = "{day}/{month}/{year}".format(day = today.day, month = today.month, year = today.year)
    
    for l in logs:
        if l["date"] != date:
            log = l
    else:
        if log:
            response = Response[EmailLog](data = EmailLog(**log) , code = 200, message = "Log returned")
        else:
            response = Response[EmailLog](data = None, code = 200, message = "Today's emails not sent yet")
            
    return response