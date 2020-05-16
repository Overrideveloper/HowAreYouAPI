import uvicorn
from dotenv import load_dotenv
from pathlib import Path

if __name__ == "__main__":
    env_path = Path('.') / '.local.env'
    load_dotenv(dotenv_path=env_path, override=True)

    uvicorn.run("src:app", host="127.0.0.1", port=8000, log_level="info", reload=True)