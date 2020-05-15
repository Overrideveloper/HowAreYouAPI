import pytest
from dotenv import load_dotenv
from pathlib import Path

def setup():
    env_path = Path('.') / '.local.test.env'
    load_dotenv(dotenv_path=env_path, override=True)
    
def teardown():
    from src.constants import ADDRESS_KEY, ANSWERS_KEY, EMAIL_LOG_KEY, QUESTIONS_KEY, USERS_KEY
    from src.db import Database
    
    db = Database()
    
    db.remove(ADDRESS_KEY)
    db.remove(ANSWERS_KEY)
    db.remove(EMAIL_LOG_KEY)
    db.remove(QUESTIONS_KEY)
    db.remove(USERS_KEY)

if __name__ == "__main__":
    setup()

    pytest.main(['tests/integration'])
    
    teardown()
