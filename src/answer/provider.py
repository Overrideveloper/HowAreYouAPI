from src.answer.models import Answer
from src.question.models import Question
from src.constants import ANSWERS_KEY, QUESTIONS_KEY
from src.utils import randomInt
from src.response_models import Response
from typing import List
import src.db as db

def getAnswers() -> Response:
    data: List[Answer] = db.get(ANSWERS_KEY) or []
    return { "data": data, "code": 200, "message": "{0} Answer(s) returned".format(len(data)) }

def getAnswer(id: int) -> Response:
    answers: List[Answer] = db.get(ANSWERS_KEY) or []
    answer: Answer = None
    
    for a in answers:
        if a["id"] == id:
            answer = a
    else:
        if answer:
            return { "data": answer, "code": 200, "message": "Answer returned" }
        else:
            return { "data": None, "code": 404, "message": "Answer not found" }
    
def addAnswer(req: dict) -> Response:
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question: Question = None
    
    for q in questions:
        if q["id"] == req["question_id"]:
            question = q
    else:
        if question:
            answers: List[Answer] = db.get(ANSWERS_KEY) or []
            question_already_answered: bool = False
            
            for a in answers:
                if a["question_id"] == question["id"]:
                    question_already_answered = True
            else:
                if not question_already_answered:
                    answer = dict(Answer(answer = req["answer"], question_id = question["id"], id = randomInt()))
                    
                    answers.append(answer)
                    db.set(ANSWERS_KEY, answers)

                    return { "data": answer, "code": 201, "message": "Answer saved" }
                else:
                    return { "data": None, "code": 400, "message": "Question already answered" }
        else:
            return { "data": None, "code": 404, "message": "Question not found" }
 
def deleteAnswer(id: int) -> Response:
    answers: List[Answer] = db.get(ANSWERS_KEY) or []
    answer_index = None
    
    for i in range(len(answers)):
        if answers[i]["id"] == id:
            answer_index = i
    else:
        if answer_index is not None:
            del answers[answer_index]
            db.set(ANSWERS_KEY, answers)

            return { "data": None, "code": 200, "message": "Answer deleted" }
        else:
            return { "data": None, "code": 404, "message": "Answer not found" }

def editAnswer(id: int, req: dict) -> Response:
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question: Question = None
    
    for q in questions:
        if q["id"] == req["question_id"]:
            question = q
    else:
        if question:
            answers: List[Answer] = db.get(ANSWERS_KEY) or []
            answer_index = None
            
            for i in range(len(answers)):
                if answers[i]["id"] == id:
                    answer_index = i
            else:
                if answer_index is not None:
                    answer = answers[answer_index]
                    answer["question_id"] = question["id"]
                    answer["answer"] = req["answer"]
                    
                    del answers[answer_index]

                    answers.insert(answer_index, answer)
                    db.set(ANSWERS_KEY, answers)
                    
                    return { "data": answer, "code": 200, "message": "Answer modified" }
                else:
                    return { "data": None, "code": 404, "message": "Answer not found" }
        else:
            return { "data": None, "code": 404, "message": "Question not found" }
