import src.utils as utils
from src.response_models import Response 
from typing import List, Dict

class TestGeneratorUtils:
    def test_random_int_generator(self):
        num = utils.randomInt()
        
        assert num
        assert num >= 1000
        assert num <= 9999
        
    def test_random_alphanumeric_str_generator(self):
        string = utils.randomAlphanumericStr(8)
        
        assert string
        assert len(string) == 8
        
    def test_generate_404_res_content(self):
        res = utils.generate404ResContent("Generator")
        
        assert res
        assert res["model"] == Response
        assert res["content"]
        assert res["content"]["application/json"]
        assert res["content"]["application/json"]["example"]
        assert res["content"]["application/json"]["example"]["code"] == 404
        assert not res["content"]["application/json"]["example"]["data"]
        assert res["content"]["application/json"]["example"]["message"] == "Generator not found"
        
    def test_generate_400_res_content(self):
        res = utils.generate400ResContent()
        
        assert res
        assert res["model"] == Response[List[Dict[str, str]]]
        assert res["content"]
        assert res["content"]["application/json"]
        assert res["content"]["application/json"]["example"]
        assert res["content"]["application/json"]["example"]["code"] == 400
        assert res["content"]["application/json"]["example"]["data"]
        assert isinstance(res["content"]["application/json"]["example"]["data"], list)
        assert len(res["content"]["application/json"]["example"]["data"]) == 1
        
    def test_generate_403_res_content(self):
        error = "You cannot access this resource"
        res = utils.generate403ResContent(error)
        
        assert res
        assert res["model"] == Response
        assert res["content"]
        assert res["content"]["application/json"]
        assert res["content"]["application/json"]["example"]
        assert res["content"]["application/json"]["example"]["code"] == 403
        assert not res["content"]["application/json"]["example"]["data"]
        assert res["content"]["application/json"]["example"]["message"] == error