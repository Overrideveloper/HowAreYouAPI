from fastapi.testclient import TestClient
from src.server import app

class Test0_IndexEndpoints:
    client = TestClient(app)
    
    def test_index_endpoint(self):
        response = self.client.get("/")
        
        assert response.status_code == 200
        assert response.json() == { "description": "HowAreYou Service API" }
