from fastapi import APIRouter
from typing import List
from src.constants import QUESTIONS
from src.response_models import Response

questions = APIRouter()

@questions.get('/', response_model = Response, status_code = 200)
def getQuestions():
    return { "data": QUESTIONS, "code": 200, "message": "Questions returned"}
    
    