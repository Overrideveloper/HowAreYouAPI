from tests.unit.mocks import DatabaseMock, EmailHelperMock
from src.modules.user import UserProvider, User, TokenPayload, SignupLoginUser, ChangePassword, ResetPassword, LoginResponse
from src.response_models import Response
from typing import List
from src.abstract_defs import IDatabase, IEmailHelper
from src.constants import USERS_KEY
from copy import deepcopy
import bcrypt

class TestUserProvider:
    dbMock: IDatabase = DatabaseMock()
    userProvider: UserProvider = UserProvider(dbMock, EmailHelperMock())
    user_list: List[dict] = list([
        User(id = 1, email = "john@doe.com", password = "$2b$12$wFw5u4uDUoFYjKBR04mFu.AOlbxK6oGeo7.UZZ7AP8Vix/IscmgR.").dict()
    ])
    
    def test_creation(self):
        assert self.userProvider is not None
        
    def test_signup_403(self):
        self.dbMock.set(USERS_KEY, deepcopy(self.user_list))
        
        req = SignupLoginUser(email = "mary@poppins.com", password = "maryispoppingagain")
        
        res = self.userProvider.signup(req)
        
        assert isinstance(res, Response)
        assert res.code == 403
        assert not res.data
        
        self.dbMock.remove(USERS_KEY)
        
    def test_signup_201(self):
        req = SignupLoginUser(email = "mary@poppins.com", password = "maryispoppingagain")
        
        res = self.userProvider.signup(req)
        
        assert isinstance(res, Response[LoginResponse])
        assert res.code == 201
        assert isinstance(res.data, LoginResponse)
        assert res.data.email == req.email
        assert res.data.token
        
        self.dbMock.remove(USERS_KEY)
        
    def test_login_404(self):
        self.dbMock.set(USERS_KEY, deepcopy(self.user_list))

        req = SignupLoginUser(email = "mary@poppins.com", password = "maryispoppingagain")
        res = self.userProvider.login(req)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(USERS_KEY)
        
    def test_login_200(self):
        self.dbMock.set(USERS_KEY, deepcopy(self.user_list))

        req = SignupLoginUser(email = "john@doe.com", password = "johndoe")
        res = self.userProvider.login(req)
        
        assert isinstance(res, Response[LoginResponse])
        assert res.code == 200
        assert isinstance(res.data, LoginResponse)
        assert res.data.email == req.email
        assert res.data.token
        
        self.dbMock.remove(USERS_KEY)
        
    def test_change_password_404(self):
        self.dbMock.set(USERS_KEY, deepcopy(self.user_list))
        
        req = ChangePassword(old_password = "johnsondoe", new_password = "doejohn")
        res = self.userProvider.changePassword(1, req)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(USERS_KEY)
        
    def test_change_password_200(self):
        self.dbMock.set(USERS_KEY, deepcopy(self.user_list))
        
        req = ChangePassword(old_password = "johndoe", new_password = "doejohn")
        res = self.userProvider.changePassword(1, req)
        
        assert isinstance(res, Response[bool])
        assert res.code == 200
        assert res.data is True
        
        self.dbMock.remove(USERS_KEY)
    
    def test_reset_password_404(self):
        self.dbMock.set(USERS_KEY, deepcopy(self.user_list))
        
        req = ResetPassword(email = "mary@poppins.com")
        res = self.userProvider.resetPassword(req)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(USERS_KEY)
    
    def test_reset_password_200(self):
        self.dbMock.set(USERS_KEY, deepcopy(self.user_list))
        
        req = ResetPassword(email = "john@doe.com")
        res = self.userProvider.resetPassword(req)
        
        assert isinstance(res, Response[bool])
        assert res.code == 200
        assert res.data is True
        
        self.dbMock.remove(USERS_KEY)
        
    def test_user_exist_200_true(self):
        self.dbMock.set(USERS_KEY, deepcopy(self.user_list))
        
        res = self.userProvider.doesUserExist()
        
        assert isinstance(res, Response[bool])
        assert res.code == 200
        assert res.data is True
        
        self.dbMock.remove(USERS_KEY)
        
    def test_user_exist_200_false(self):
        res = self.userProvider.doesUserExist()
        
        assert isinstance(res, Response[bool])
        assert res.code == 200
        assert not res.data
        
        self.dbMock.remove(USERS_KEY)
