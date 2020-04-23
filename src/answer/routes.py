from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.answer.request_models import AddEditAnswer as Answer
import src.answer.provider as provider

answer = APIRouter()

@answer.get('/')
def getAnswers():
    data: Response = provider.getAnswers()
    return JSONResponse(content=data, status_code=data["code"])

@answer.get('/{id}')
def getAnswer(id: int):
    data: Response = provider.getAnswer(id)
    return JSONResponse(content=data, status_code=data["code"])

@answer.post('/')
def addAnswer(payload: Answer):
    data: Response = provider.addAnswer(dict(payload))
    return JSONResponse(content=data, status_code=data["code"])

@answer.delete('/{id}')
def deleteAnswer(id: int):
    data: Response = provider.deleteAnswer(id)
    return JSONResponse(content=data, status_code=data["code"])
    
@answer.put('/{id}')
def editAnswer(id: int, payload: Answer):
    data: Response = provider.editAnswer(id, dict(payload))
    return JSONResponse(content=data, status_code=data["code"])
