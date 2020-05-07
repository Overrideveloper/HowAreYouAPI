from src.email_log.models import EmailLog
from src.constants import EMAIL_LOG_KEY
from typing import List
from src.utils import randomInt
from datetime import date as _date
from src.response_models import Response
import src.db as db

def addTodayLog(count: int):
    logs: List[EmailLog] = db.get(EMAIL_LOG_KEY) or []
    
    today = _date.today()
    date = "{day}/{month}/{year}".format(day = today.day, month = today.month, year = today.year)

    log = dict(EmailLog(id = randomInt(), date = date, count = count))
    
    logs.append(log)
    db.set(EMAIL_LOG_KEY, logs)

def getTodaysLog() -> Response:
    logs: List[EmailLog] = db.get(EMAIL_LOG_KEY) or []
    
    today = _date.today()
    date = "{day}/{month}/{year}".format(day = today.day, month = today.month, year = today.year)
    
    log: EmailLog = None
    
    for l in logs:
        if l["date"] == date:
            log = l
    else:
        if log:
            return { "data": log, "code": 200, "message": "Log returned" }
        else:
            return { "data": None, "code": 200, "message": "Today's emails not sent yet" }