import pytest
from fastapi.testclient import TestClient
from src import app

client = TestClient(app)

@pytest.fixture
def user_data(request):
    data: tuple = request.config.cache.get("user_data", None)
    
    if not data:
        res = client.post("/api/auth/login", json={ "email": "johndoe@doe.com", "password": "johndoe" })
        
        if res.status_code == 200: 
            payload = res.json()["data"]
            
            data = (payload["token"], payload["id"])
            request.config.cache.set("user_data", data)
    
    return data

@pytest.fixture
def address_id(request, user_data):
    val: int = request.config.cache.get("address_id", None)

    if not val:
        token = user_data[0]
        res = client.get('/api/address', headers={"Authorization": f"Bearer {token}"})
        
        if res.status_code == 200 and len(res.json()["data"]):
            val = res.json()["data"][0]["id"]
            request.config.cache.set("address_id", val)
    
    return val

@pytest.fixture
def question_ids(request, user_data):
    val: tuple = request.config.cache.get("question_ids", None)

    if not val:
        token = user_data[0]
        res = client.get('/api/question', headers={"Authorization": f"Bearer {token}"})
        
        if res.status_code == 200 and len(res.json()["data"]):
            val = tuple([data["id"] for data in res.json()["data"]])
            request.config.cache.set("question_ids", val)
    
    return val

@pytest.fixture
def answer_id(request, user_data):
    val: int = request.config.cache.get("answer_id", None)

    if not val:
        token = user_data[0]
        res = client.get('/api/answer', headers={"Authorization": f"Bearer {token}"})
        
        if res.status_code == 200 and len(res.json()["data"]):
            val = res.json()["data"][0]["id"]
            request.config.cache.set("answer_id", val)
    
    return val
