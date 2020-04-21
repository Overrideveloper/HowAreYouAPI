from fastapi import FastAPI
from src.answer.routes import answer
from src.question.routes import question
from src.address.routes import address
import src.email_log.provider as log_provider

app = FastAPI()

@app.get('/')
def index():
    return { "description": "HowAreYou Service API" }


@app.get('/api/log/today')
def getTodaysEmailLog():
    return log_provider.getTodayLog()

app.include_router(answer, prefix="/api/answer", tags=["answer"])
app.include_router(question, prefix="/api/question", tags=["question"])
app.include_router(address, prefix="/api/address", tags=["address"])