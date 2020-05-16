from src.jwt import encodeJWT, decodeJWT, JWTBearer
from src.modules.user import SignupLoginUser, UserProvider
from tests.unit.mocks import DatabaseMock, EmailHelperMock
from src.constants import USERS_KEY

class TestJWTUtils:
    baseDict = { "animal": "fox", "color": "brown", "speed": "quick" }
    dbMock = DatabaseMock()
    
    def test_jwt_payload_encode(self):
        token = encodeJWT(self.baseDict)

        assert token
        assert isinstance(token, str)
        
    def test_jwt_str_decode(self):
        token = encodeJWT(self.baseDict)
        payload = decodeJWT(token)
        
        assert payload
        assert isinstance(payload, dict)
        assert payload == self.baseDict
        
    def test_jwt_verify(self):
        def createUserAndGetToken() -> str:
            req = SignupLoginUser(email = "mary@poppins.com", password = "maryispoppingagain")

            return UserProvider(self.dbMock, EmailHelperMock()).signup(req).data.token
        
        def verifyJWT():
            validity = JWTBearer(self.dbMock).verify_jwt(createUserAndGetToken())

            assert validity
            
        def teardown():
            self.dbMock.remove(USERS_KEY)
            
        verifyJWT()
        teardown()
        