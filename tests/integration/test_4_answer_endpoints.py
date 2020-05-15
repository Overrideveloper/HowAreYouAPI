from fastapi.testclient import TestClient
from src.server import app
from src.response_models import Response
from src.modules.answer.models import Answer
import os

URL_FRAGMENT = "/api/answer"

class Test4_AnswerEndpoints:
    client = TestClient(app)

    def test_get_answers_empty(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.get(URL_FRAGMENT, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert len(res.json()["data"]) == 0
    
    def test_get_answer_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.get(f"{URL_FRAGMENT}/8375", headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Answer not found").dict()
     
    def test_create_answer_question_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.post(URL_FRAGMENT, json={ "question_id": 9243, "answer": "I am well"}, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Question not found").dict()
    
    def test_create_answers_successful(self):
        token = os.environ.get("TEST_TOKEN")
        question_id = int(os.environ.get("TEST_QUESTION_ID"))
        question_id_1 = int(os.environ.get("TEST_QUESTION_ID_1"))
        
        res = self.client.post(URL_FRAGMENT, json={ "question_id": question_id, "answer": "I am well"}, headers={"Authorization": f"Bearer {token}"})
        res1 = self.client.post(URL_FRAGMENT, json={ "question_id": question_id_1, "answer": "It is good"}, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 201
        assert res.json()["data"]["question_id"] == question_id
        assert res.json()["data"]["answer"] == "I am well"
        
        assert res1.status_code == 201
        assert res1.json()["data"]["question_id"] == question_id_1
        assert res1.json()["data"]["answer"] == "It is good"
        
        os.environ["TEST_ANSWER_ID"] = str(res.json()["data"]["id"])
        
    def test_create_answer_question_already_answered(self):
        token = os.environ.get("TEST_TOKEN")
        question_id = int(os.environ.get("TEST_QUESTION_ID"))
        res = self.client.post(URL_FRAGMENT, json={ "question_id": question_id, "answer": "I am not well"}, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 403
        assert res.json() == Response(data = None, code = 403, message = "Question already answered").dict()

    def test_edit_answer_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.put(f"{URL_FRAGMENT}/8375", json={ "answer": "I am very well" }, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Answer not found").dict()

    def test_edit_answer_successful(self):
        token = os.environ.get("TEST_TOKEN")
        answer_id = int(os.environ.get("TEST_ANSWER_ID"))
        res = self.client.put(f"{URL_FRAGMENT}/{answer_id}", json={ "answer": "I am very well" }, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 200
        assert res.json()["message"] == "Answer modified"
        assert res.json()["data"]["id"] == answer_id
        assert res.json()["data"]["answer"] == "I am very well"

    def test_delete_answer_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.delete(f"{URL_FRAGMENT}/8375", headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Answer not found").dict()

    def test_delete_successful(self):
        token = os.environ.get("TEST_TOKEN")
        answer_id = int(os.environ.get("TEST_ANSWER_ID"))
        res = self.client.delete(f"{URL_FRAGMENT}/{answer_id}", headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 200
        assert res.json() == Response(data = None, code = 200, message = "Answer deleted").dict()
    