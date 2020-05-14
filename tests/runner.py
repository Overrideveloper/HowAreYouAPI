import sys
import pytest
from dotenv import load_dotenv
from pathlib import Path

if __name__ == "__main__":
    env_path = Path('.') / '.local.test.env'
    load_dotenv(dotenv_path=env_path, override=True)

    pytest.main(sys.argv[1:])