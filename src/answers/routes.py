from fastapi import APIRouter, HTTPException
from typing import List, Any
from src.answers.models import Answer
from src.response_models import Response
from src.constants import QUESTIONS as questions

answers = APIRouter()



_answers: List[Answer] = []

@answers.get('/', response_model=Response, status_code = 200)
def getAnswers():
    return { "data": _answers, "code": 200, "message": "Answers returned" }

@answers.get('/', response_model=Response, status_code = 200)
def getAnswers():
    return { "data": _answers, "code": 200, "message": "Answers returned" }

@answers.post('/', response_model=Response, status_code = 201)
async def addAnswers(_payload: Answer):
    payload = dict(_payload)

    if payload["question"] in questions:
        question_index: int = questions.index(payload["question"])
        
        if payload["answer"]:
            answer_index: int = None
            
            for i in range(len(_answers)):
                if _answers[i]["question"] == payload["question"]:
                    answer_index = i
            else:
                if answer_index is not None:
                    del _answers[i]
                    _answers.insert(i, payload)
                else:
                    _answers.append(payload)

            return { "data": payload, "code": 201, "message": "Answer saved" }
        else:
            raise HTTPException(status_code = 400, detail = "Answer cannot be empty")
    else:
        raise HTTPException(status_code = 400, detail = "'{question}' is not a valid question".format(question = payload["question"]))
        