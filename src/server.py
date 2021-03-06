from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .exceptions_handlers import validationExceptionHandler, httpExceptionHandler
from src.modules.answer import answerRouter
from src.modules.question import questionRouter
from src.modules.address import addressRouter
from src.modules.user import userRouter
from src.jwt import JWTBearer
from src.scheduler import SEND_EMAIL_TO_ADDRESSES, RESET_ANSWERS
from src.response_models import Response
from src.modules.email_log import EmailLog
from src.modules.email_log import EmailLogProvider
from src.db import Database
from typing import Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

app = FastAPI()
jwt_bearer = JWTBearer(Database())
emailLogProvider = EmailLogProvider(Database())

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return validationExceptionHandler(exc)

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return httpExceptionHandler(request, exc)

@app.on_event("startup")
def startup():
    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    scheduler.start()
    scheduler.add_job(SEND_EMAIL_TO_ADDRESSES, "cron", hour=14, minute=30, id=SEND_EMAIL_TO_ADDRESSES.__name__)
    scheduler.add_job(RESET_ANSWERS, "cron", hour=0, id=RESET_ANSWERS.__name__)

@app.get('/', tags=["Index"], response_model=Dict[str, str])
def index():
    return { "description": "HowAreYou Service API" }

@app.get('/api/log/today', tags=["Email Log"], summary="Get Today's Email Log", description="Get email log information for today.", response_model=Response[EmailLog],
dependencies=[Depends(jwt_bearer)])
def getTodaysEmailLog():
    return emailLogProvider.getTodaysLog()


app.include_router(answerRouter, prefix="/api/answer", tags=["Answer"], dependencies=[Depends(jwt_bearer)])
app.include_router(questionRouter, prefix="/api/question", tags=["Question"], dependencies=[Depends(jwt_bearer)])
app.include_router(addressRouter, prefix="/api/address", tags=["Address"], dependencies=[Depends(jwt_bearer)])
app.include_router(userRouter, prefix="/api/auth", tags=["Auth"])