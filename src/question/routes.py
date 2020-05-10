from fastapi import APIRouter, Path, Body
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.question.request_models import AddEditQuestion as ReqQuestion
from src.question.models import Question
import src.question.provider as provider
from typing import List, Union
from src.utils import generate404ResContent, generate400ResContent

question = APIRouter()

@question.get('/', summary="Get Questions", description="Get a list of all questions", response_model=Response[List[Question]])
def getQuestions():
    data: Response[List[Question]] = provider.getQuestions()

    return JSONResponse(content = data.dict(), status_code = data.code)

@question.get('/{id}', summary="Get Question", description="Get a question", response_model=Response[Question],
responses={ 404: generate404ResContent("Question"), 400: generate400ResContent(), 422: {} })
def getQuestion(id: int = Path(..., description="The ID of the question to get")):
    data: Union[Response[Question], Response] = provider.getQuestion(id)

    return JSONResponse(content = data.dict(), status_code = data.code)

@question.post('/', summary="Add Question", description="Create and save a question", response_model=Response[Question],
responses={ 400: generate400ResContent(), 422: {} })
def addQuestion(payload: ReqQuestion = Body(..., description="The question to be created")):
    data: Union[Response[Question], Response] = provider.addQuestion(payload)

    return JSONResponse(content = data.dict(), status_code = data.code)

@question.delete('/{id}', summary="Delete Question", description="Delete a question", response_model=Response,
responses={ 404: generate404ResContent("Question"), 400: generate400ResContent(), 422: {} })
def deleteQuestion(id: int = Path(..., description="The ID of the question to delete")):
    data: Response = provider.deleteQuestion(id)

    return JSONResponse(content = data.dict(), status_code = data.code)

@question.put('/{id}', summary="Edit Question", description="Edit a question", response_model=Response[Question],
responses={ 404: generate404ResContent("Question"), 400: generate400ResContent(), 422: {} })
def editQuestion(id: int = Path(..., description="The ID of the question to edit"), payload: ReqQuestion = Body(..., description="The question data to be used in the edit")):
    data: Union[Response[Question], Response] = provider.editQuestion(id, payload)

    return JSONResponse(content = dict(data), status_code = data.code)