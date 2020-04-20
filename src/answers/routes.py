from fastapi import APIRouter, Response as HttpResponse
from src.response_models import Response
from src.answers.request_models import AddEditAnswer as Answer
import src.answers.provider as provider

answers = APIRouter()

@answers.get('/', response_model = Response, status_code = 200)
def getAnswers():
    data = provider.getAnswers()
    return { "data": data, "code": 200, "message": "{0} Answer(s) returned".format(len(data)) }

@answers.get('/{id}', response_model = Response, status_code = 200)
def getAnswer(id: int, response: HttpResponse):
    data = provider.getAnswer(id)
    
    if data is not None:
        return { "data": data, "code": 200, "message": "Answer returned" }
    else:
        response.status_code = 404

        return { "data": None, "code": 404, "message": "Answer not found" }

@answers.post('/', response_model = Response, status_code = 201)
def addAnswer(payload: Answer, response: HttpResponse):
    data = provider.addAnswer(dict(payload))
    
    if data["code"] == 200:
        return { "data": data["data"], "code": 200, "message": "Answer saved" }
    else:
        response.status_code = data["code"]

        return { "data": None, "code": data["code"], "message": data["message"] }

@answers.delete('/{id}', response_model = Response, status_code = 200)
def deleteAnswer(id: int, response: HttpResponse):
    data = provider.deleteAnswer(id)
    
    if data is not None:
        return { "data": None, "code": 200, "message": "Answer deleted" }
    else:
        response.status_code = 404

        return { "data": None, "code": 404, "message": "Answer not found" }
    
@answers.put('/{id}', response_model = Response, status_code = 200)
def editAnswer(id: int, payload: Answer, response: HttpResponse):
    data = provider.editAnswer(id, dict(payload))
    
    if data["code"] == 200:
        return { "data": data["data"], "code": 200, "message": "Answer edited" }
    else:
        response.status_code = data["code"]

        return { "data": None, "code": data["code"], "message": data["message"] }
    