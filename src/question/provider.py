from src.question.models import Question
from src.constants import QUESTIONS_KEY
from typing import List
from src.utils import randomInt
import src.db as db
    
def getQuestions():
    data: List[Question] = db.get(QUESTIONS_KEY) or []
    return { "data": data, "code": 200, "message": "{0} Question(s) returned".format(len(data)) }

def getQuestion(id: int):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question: Question = None
    
    for q in questions:
        if q["id"] == id:
            question = q
    else:
        if question:
            return { "data": question, "code": 200, "message": "Question returned" }
        else:
            return { "data": None, "code": 404, "message": "Question not found" }
    
def addQuestion(req: dict):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question = dict(Question(question = req["question"], defaultAnswer = req["defaultAnswer"], id = randomInt()))
    
    questions.append(question)
    db.set(QUESTIONS_KEY, questions)

    return { "data": question, "code": 200, "message": "Question saved" }

def deleteQuestion(id: int):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question_index = None
    
    for i in range(len(questions)):
        if questions[i]["id"] == id:
            question_index = i
    else:
        if question_index: 
            del questions[question_index]
            db.set(QUESTIONS_KEY, questions)

            return { "data": None, "code": 200, "message": "Question deleted" }
        else:
            return { "data": None, "code": 404, "message": "Question not found" }

def editQuestion(id: int, req: dict):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question_index = None
    
    for i in range(len(questions)):
        if questions[i]["id"] == id:
            question_index = i
    else:
        if question_index:
            question = questions[question_index]
            question["question"] = req["question"]
            question["defaultAnswer"] = req["defaultAnswer"]
            
            del questions[question_index]

            questions.insert(question_index, question)
            db.set(QUESTIONS_KEY, questions)
                    
            return { "data": question, "code": 200, "message": "Question modified" }
        else:
            return { "data": None, "code": 404, "message": "Question not found" }