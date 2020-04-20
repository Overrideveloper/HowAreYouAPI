from fastapi import APIRouter, Response as HttpResponse
from src.response_models import Response
from src.questions.request_models import AddEditQuestion as Question
import src.questions.provider as provider

questions = APIRouter()

@questions.get('/', response_model = Response, status_code = 200)
def getQuestions():
    data = provider.getQuestions()
    return { "data": data, "code": 200, "message": "{0} Question(s) returned".format(len(data)) }

@questions.get('/{id}', response_model = Response, status_code = 200)
def getQuestion(id: int, response: HttpResponse):
    data = provider.getQuestion(id)
    
    if data is not None:
        return { "data": data, "code": 200, "message": "Question returned" }
    else:
        response.status_code = 404

        return { "data": None, "code": 404, "message": "Question not found" }

@questions.post('/', response_model = Response, status_code = 201)
def addQuestion(payload: Question):
    data = provider.addQuestion(dict(payload))
    
    return { "data": data, "code": 201, "message": "Question saved"}

@questions.delete('/{id}', response_model = Response, status_code = 200)
def deleteQuestion(id: int, response: HttpResponse):
    data = provider.deleteQuestion(id)
    
    if data is not None:
        return { "data": None, "code": 200, "message": "Question deleted" }
    else:
        response.status_code = 404
        
        return { "data": None, "code": 404, "message": "Question not found" }

@questions.put('/{id}', response_model = Response, status_code = 200)
def editQuestion(id: int, payload: Question, response: HttpResponse):
    data = provider.editQuestion(id, dict(payload))
    
    if data is not None:
        return { "data": data, "code": 200, "message": "Question edited" }
    else:
        response.status_code = 404

        return { "data": None, "code": 404, "message": "Question not found" }
