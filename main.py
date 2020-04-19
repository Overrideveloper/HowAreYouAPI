from fastapi import FastAPI
from src.answers.routes import answers
from src.questions.routes import questions

app = FastAPI()

@app.get('/')
def index():
    return { "description": "HowAreYou API by Overrideveloper" }

app.include_router(answers, prefix="/api/answer", tags=["answer"])
app.include_router(questions, prefix="/api/question", tags=["question"])