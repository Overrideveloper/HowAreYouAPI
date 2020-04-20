from src.questions.models import Question
from src.constants import QUESTIONS_KEY
from typing import List, Dict
from src.utils import randomInt
import src.db as db
    
def getQuestions():
    return db.get(QUESTIONS_KEY) or []

def getQuestion(id: int):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question: Question = None
    
    for q in questions:
        if q["id"] == id:
            question = q
    else:
        return question
    
def addQuestion(req: Dict):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question = dict(Question(question = req["question"], defaultAnswer = req["defaultAnswer"], id = randomInt()))
    
    questions.append(question)
    db.set(QUESTIONS_KEY, questions)
    return question

def deleteQuestion(id: int):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question_index = None
    
    for i in range(len(questions)):
        if questions[i]["id"] == id:
            question_index = i
    else:
        if question_index is not None: 
            question = questions[question_index]
            del questions[question_index]
            db.set(QUESTIONS_KEY, questions)
            return question
        else:
            return None
            
def editQuestion(id: int, req: Dict):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question_index = None
    
    for i in range(len(questions)):
        if questions[i]["id"] == id:
            question_index = i
    else:
        if question_index is not None:
            question = questions[question_index]
            question["question"] = req["question"]
            question["defaultAnswer"] = req["defaultAnswer"]
            
            del questions[question_index]

            questions.insert(question_index, question)
            db.set(QUESTIONS_KEY, questions)
            
            return question
        else:
            return None