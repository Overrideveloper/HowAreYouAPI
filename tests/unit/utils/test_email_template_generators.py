from src.email import genDailyAnswerBlock, genDailyAnswers, genPasswordResetEmail, daily_answer_block, daily_answers, password_reset
from src.constants import SUBJECT_TWITTER, SUBJECT_NAME

class TestEmailTemplateGenerators:
    def test_gen_daily_answer_block(self):
        question = "How are you?"
        answer = "Fine"

        block = genDailyAnswerBlock(question, answer)
        
        assert block
        assert block.index(question) > -1
        assert block.index(answer) > -1
        assert block == daily_answer_block.format(question=question, answer=answer)
        
    def test_gen_daily_answers(self):
        name = "Jordan"
        answers = "ANSWERS_PLACEHOLDER"
        
        block = genDailyAnswers(name, answers)
        
        assert block
        assert block.index(name) > -1
        assert block.index(answers) > -1
        assert block.index(SUBJECT_NAME) > 1
        assert block.index(SUBJECT_TWITTER) > 1
        assert block == daily_answers.format(name=name, answers=answers, subject=SUBJECT_NAME, twitter_handle=SUBJECT_TWITTER)
        
    def test_gen_password_reset_email(self):
        password = "Habachi"
        
        block = genPasswordResetEmail(password)
        
        assert block
        assert block.index(password) > -1
        assert block.index(SUBJECT_NAME) > -1
        assert block == password_reset.format(subject=SUBJECT_NAME, password=password)