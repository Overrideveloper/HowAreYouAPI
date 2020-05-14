import os

REDIS = { "HOST": os.getenv("REDIS_HOST") , "PORT": os.getenv("REDIS_PORT") }

ANSWERS_KEY = os.getenv("ANSWERS_KEY")
QUESTIONS_KEY = os.getenv("QUESTIONS_KEY")
ADDRESS_KEY = os.getenv("ADDRESS_KEY")
EMAIL_LOG_KEY = os.getenv("EMAIL_LOG_KEY")
USERS_KEY = os.getenv("USERS_KEY")

JWT_SECRET = os.getenv("JWT_SECRET")

SENDGRID_KEY = os.getenv("SENDGRID_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SUBJECT_NAME = os.getenv("SUBJECT_NAME")
SUBJECT_TWITTER = os.getenv("SUBJECT_TWITTER")