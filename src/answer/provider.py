from src.answer.models import Answer
from src.answer.request_models import AddEditAnswer as ReqAnswer
from src.question.models import Question
from src.constants import ANSWERS_KEY, QUESTIONS_KEY
from src.utils import randomInt
from src.response_models import Response

from typing import List
import src.db as db

def getAnswers() -> Response:
    data: List[dict] = db.get(ANSWERS_KEY) or []

    return Response(data = data, code = 200, message = "{0} Answer(s) returned".format(len(data)))

def getAnswer(id: int) -> Response:
    answers: List[dict] = db.get(ANSWERS_KEY) or []
    response: Response = None
    answer: dict = None
    
    for answ in answers:
        if answ["id"] == id:
            answer = answ
    else:
        if answer:
            response = Response(data = answer, code = 200, message = "Answer returned")
        else:
            response = Response(data = None, code = 404, message = "Answer not found")
    
    return response
    
def addAnswer(req: ReqAnswer) -> Response:
    questions: List[dict] = db.get(QUESTIONS_KEY) or []
    response: Response = None
    question: dict = None
    
    for ques in questions:
        if ques["id"] == req.question_id:
            question = ques
    else:
        if question:
            answers: List[dict] = db.get(ANSWERS_KEY) or []
            question_already_answered: bool = False
            
            for answ in answers:
                if answ["question_id"] == question["id"]:
                    question_already_answered = True
            else:
                if not question_already_answered:
                    answer = Answer(answer = req.answer, question_id = req.question_id, id = randomInt())
                    
                    answers.append(dict(answer))
                    db.set(ANSWERS_KEY, answers)

                    response = Response(data = dict(answer), code = 201, message = "Answer saved")
                else:
                    response = Response(data = None, code = 400, message = "Question already answered")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
    
    return response
 
def deleteAnswer(id: int) -> Response:
    answers: List[dict] = db.get(ANSWERS_KEY) or []
    answer_index: int = None
    response: Response = None
    
    for i in range(len(answers)):
        if answers[i]["id"] == id:
            answer_index = i
    else:
        if answer_index is not None:
            del answers[answer_index]
            db.set(ANSWERS_KEY, answers)

            response = Response (data = None, code = 200, message = "Answer deleted")
        else:
            response = Response(data = None, code = 404, message = "Answer not found")
    
    return response

def editAnswer(id: int, req: ReqAnswer) -> Response:
    questions: List[dict] = db.get(QUESTIONS_KEY) or []
    question: Question = None
    response: Response = None
    
    for ques in questions:
        if ques["id"] == req.question_id:
            question = ques
    else:
        if question:
            answers: List[dict] = db.get(ANSWERS_KEY) or []
            answer_index: int = None
            
            for i in range(len(answers)):
                if answers[i]["id"] == id:
                    answer_index = i
            else:
                if answer_index is not None:
                    answer = answers[answer_index]
                    answer["question_id"] = question["id"]
                    answer["answer"] = req.answer
                    
                    del answers[answer_index]

                    answers.insert(answer_index, answer)
                    db.set(ANSWERS_KEY, answers)
                    
                    response = Response(data = answer, code = 200, message = "Answer modified")
                else:
                    response = Response(data = None, code = 404, message = "Answer not found")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
    
    return response

def deleteAllAnswers():
    db.remove(ANSWERS_KEY)