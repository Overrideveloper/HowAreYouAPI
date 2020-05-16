from fastapi.testclient import TestClient
from src import app
from src.response_models import Response
from src.modules.question import Question
import os

URL_FRAGMENT = "/api/question"

class Test3_QuestionEndpoints:
    client = TestClient(app)

    def test_get_questions_empty(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.get(URL_FRAGMENT, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert len(res.json()["data"]) == 0
    
    def test_get_question_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.get(f"{URL_FRAGMENT}/9243", headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Question not found").dict()
    
    def test_create_questions_successful(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.post(URL_FRAGMENT, json={ "question": "How are you?", "defaultAnswer": "I am well"}, headers={"Authorization": f"Bearer {token}"})
        res1 = self.client.post(URL_FRAGMENT, json={ "question": "How is work?", "defaultAnswer": "It is good"}, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 201
        assert res.json()["data"]["question"] == "How are you?"
        assert res.json()["data"]["defaultAnswer"] == "I am well"

        assert res1.status_code == 201
        assert res1.json()["data"]["question"] == "How is work?"
        assert res1.json()["data"]["defaultAnswer"] == "It is good"
        
        os.environ["TEST_QUESTION_ID"] = str(res.json()["data"]["id"])
        os.environ["TEST_QUESTION_ID_1"] = str(res1.json()["data"]["id"])
    
    def test_get_questions(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.get(URL_FRAGMENT, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert len(res.json()["data"]) == 2
        
    def test_get_question(self):
        token = os.environ.get("TEST_TOKEN")
        question_id = int(os.environ.get("TEST_QUESTION_ID"))

        res = self.client.get(f"{URL_FRAGMENT}/{question_id}", headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert res.json()["data"]
        assert res.json()["data"]["id"] == question_id
        
    def test_edit_question_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.put(f"{URL_FRAGMENT}/9243", json={ "question": "How are you?", "defaultAnswer": "I am not doing so well"}, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code
        assert res.json() == Response(data = None, code = 404, message = "Question not found").dict()
    
    def test_edit_question_successful(self):
        token = os.environ.get("TEST_TOKEN")
        question_id = int(os.environ.get("TEST_QUESTION_ID"))
        question = Question(id = question_id, question = "How are you?", defaultAnswer = "I am not doing so well")

        res = self.client.put(f"{URL_FRAGMENT}/{question_id}", json={ "question": question.question, "defaultAnswer": question.defaultAnswer }, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code
        assert res.json() == Response(data = question, code = 200, message = "Question modified").dict()
        
    def test_delete_question_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.delete(f"{URL_FRAGMENT}/9243", headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code
        assert res.json() == Response(data = None, code = 404, message = "Question not found").dict()
                
    def test_delete_question_successful(self):
        token = os.environ.get("TEST_TOKEN")
        question_id = int(os.environ.get("TEST_QUESTION_ID_1"))
        res = self.client.delete(f"{URL_FRAGMENT}/{question_id}", headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code
        assert res.json() == Response(data = None, code = 200, message = "Question deleted").dict()
