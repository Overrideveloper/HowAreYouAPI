from tests.unit.mocks.db_mock import DatabaseMock
from src.modules.question.provider import QuestionProvider
from src.response_models import Response
from src.modules.question.models import Question
from typing import List
from src.abstract_defs import IDatabase
from src.constants import QUESTIONS_KEY
from src.modules.question.request_models import AddEditQuestion
from copy import deepcopy

class TestQuestionProvider:
    dbMock: IDatabase = DatabaseMock()
    questionProvider: QuestionProvider = QuestionProvider(dbMock)
    question_list: List[dict] = list([
        Question(id = 1, question = "Hello?", defaultAnswer = "Hi").dict(),
        Question(id = 2, question = "How are you?", defaultAnswer = "Fine").dict(),
        Question(id = 3, question = "How do you do?", defaultAnswer = "Well").dict()
    ])
    
    def test_creation(self):
        assert self.questionProvider is not None
    
    def test_get_all_empty(self):
        res = self.questionProvider.getAll()
        
        assert isinstance(res, Response[List[Question]])
        assert res.code == 200
        assert len(res.data) == 0
        
    def test_get_all_non_empty(self):
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        res = self.questionProvider.getAll()
        
        assert isinstance(res, Response[List[Question]])
        assert res.code == 200
        assert len(res.data) == len(self.question_list)
        
        self.dbMock.remove(QUESTIONS_KEY)
                
    def test_get_200(self):
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        res = self.questionProvider.get(1)
        
        assert isinstance(res, Response[Question])
        assert res.code == 200
        assert isinstance(res.data, Question)
        assert res.data.dict() == self.question_list[0]
        
        self.dbMock.remove(QUESTIONS_KEY)
        
    def test_get_404(self):
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        res = self.questionProvider.get(99)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(QUESTIONS_KEY)

    def test_add_201(self):
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        payload = AddEditQuestion(question = "What is the time?", defaultAnswer = "6 minutes past 9")
        
        res = self.questionProvider.add(payload)
        
        assert isinstance(res, Response[Question])
        assert res.code == 201
        assert isinstance(res.data, Question)
        assert res.data == Question(id = res.data.id, **payload.dict()).dict()
        
        self.dbMock.remove(QUESTIONS_KEY)

    def test_delete_404(self):
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))
        
        res = self.questionProvider.delete(99)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(QUESTIONS_KEY)
    
    def test_delete_200(self):
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        res = self.questionProvider.delete(1)
        res1 = self.questionProvider.getAll()
        
        assert isinstance(res, Response)
        assert res.code == 200

        assert res1.code == 200
        assert len(res1.data) == 2
        assert res1.data[0] == self.question_list[1]

        self.dbMock.remove(QUESTIONS_KEY)

    def test_edit_404(self):
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))
        
        payload = AddEditQuestion(question = "What is the cube root of 8?", defaultAnswer = "2")
        
        res = self.questionProvider.edit(99, payload)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(QUESTIONS_KEY)

    def test_edit_200(self):
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))
        
        payload = AddEditQuestion(question = "What is the cube root of 8?", defaultAnswer = "2")
        
        res = self.questionProvider.edit(1, payload)
        res1 = self.questionProvider.get(1)
        
        assert isinstance(res, Response)
        assert res.code == 200
        assert res.data == Question(id = 1, **payload.dict()).dict()

        assert res1.code == 200
        assert res1.data == Question(id = 1, **payload.dict())

