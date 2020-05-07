from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.question.request_models import AddEditQuestion as ReqQuestion
import src.question.provider as provider

question = APIRouter()

@question.get('/')
def getQuestions():
    data: Response = provider.getQuestions()

    return JSONResponse(content = dict(data), status_code = data.code)

@question.get('/{id}')
def getQuestion(id: int):
    data: Response = provider.getQuestion(id)

    return JSONResponse(content = dict(data), status_code = data.code)

@question.post('/')
def addQuestion(payload: ReqQuestion):
    data: Response = provider.addQuestion(payload)

    return JSONResponse(content = dict(data), status_code = data.code)

@question.delete('/{id}')
def deleteQuestion(id: int):
    data: Response = provider.deleteQuestion(id)

    return JSONResponse(content = dict(data), status_code = data.code)

@question.put('/{id}')
def editQuestion(id: int, payload: ReqQuestion):
    data: Response = provider.editQuestion(id, payload)

    return JSONResponse(content = dict(data), status_code = data.code)