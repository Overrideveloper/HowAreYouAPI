from src.response_models import Response
from src.modules.question.models import Question
from src.modules.answer.models import Answer
from src.modules.address.models import Address
from src.constants import SUBJECT_NAME
from src.email.email_templates import genDailyAnswerBlock, genDailyAnswers
from src.db import Database
from src.modules.address.provider import AddressProvider
from src.modules.email_log.provider import EmailLogProvider
from src.modules.question.provider import QuestionProvider
from src.modules.answer.provider import AnswerProvider
from src.email.email_helper import EmailHelper

from typing import List, Union

questionProvider = QuestionProvider(Database())
logProvider = EmailLogProvider(Database())
addressProvider = AddressProvider(Database())
answerProvider = AnswerProvider(Database())
emailHelper = EmailHelper()

def SEND_EMAIL_TO_ADDRESSES():
    questionRes: Response[List[Question]] = questionProvider.getAll()
    addressRes: Response[List[Address]] = addressProvider.getAll()
    answerRes: Response[List[Answer]] = answerProvider.getAll()

    if questionRes.code == 200 and addressRes.code == 200 and answerRes.code == 200:
        questions: List[Question] = questionRes.data
        addresses: List[Address] = addressRes.data
        _answers: List[Answer] = answerRes.data

        answers = ""
        
        for question in questions:
            answer = None

            for _answer in _answers:
                if _answer.question_id == question.id:
                    answer = _answer.answer
            else:
                answers += genDailyAnswerBlock(question.question, answer if answer else question.defaultAnswer)
        else:
            successCount = 0

            for address in addresses:
                res = emailHelper.sendMail(emailHelper.createMail(address.email, f"How {SUBJECT_NAME} is doing today", genDailyAnswers(address.name, answers)))
                
                successCount += 1 if res else 0
            else:
                logProvider.addTodayLog(successCount)

def RESET_ANSWERS():
    answerProvider.deleteAll()