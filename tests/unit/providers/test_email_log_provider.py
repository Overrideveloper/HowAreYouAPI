from src.abstract_defs import IDatabase
from tests.unit.mocks.db_mock import DatabaseMock
from src.modules.email_log.provider import EmailLogProvider
from src.modules.email_log.models import EmailLog
from src.response_models import Response

class TestEmailLogProvider:
    dbMock: IDatabase = DatabaseMock()
    emailLogProvider: EmailLogProvider = EmailLogProvider(dbMock)
    
    def test_creation(self):
        assert self.emailLogProvider is not None
        
    def test_get_empty_log(self):
        res = self.emailLogProvider.getTodaysLog()
        
        assert isinstance(res, Response)
        assert res.code == 200
        assert not res.data
        
    def test_add_todays_log_and_get_non_empty_log(self):
        self.emailLogProvider.addTodayLog(5)
        
        res = self.emailLogProvider.getTodaysLog()
        
        assert isinstance(res, Response[EmailLog])
        assert res.code == 200
        assert res.data
        assert isinstance(res.data, EmailLog)
        assert res.data.count == 5