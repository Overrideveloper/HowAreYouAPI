from src.constants import SUBJECT_NAME, SUBJECT_TWITTER

daily_answers = """\
    <html>
    <body style="margin: 0; padding: 0; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans',sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'; line-height: 1.5;">
        <table align="center" border="1" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
            <tr>
                <td bgcolor="#1b053d" style="padding: 24px 32px 24px 32px;">
                    <h6 style="font-size: 22px; font-weight: 400; color: white; margin: 0;">How are you, {subject}?</h6>
                </td>
            </tr>
            <tr>
                <td bgcolor="#ffffff" style="padding: 24px 32px 24px 32px;">
                    <h2 style="margin: 0; font-weight: 400; font-size: 24px;">Hello {name}!</h2>
                    <p style="margin: 10px 0 0 0; font-weight: 300; font-size: 14px;">This is <b style="font-weight: 400;">Wisdom Banso</b> and these are today's answers to the frequently asked <b style="font-weight: 400;">"How are you?"</b>-type questions.</p>
                    
                    <div style="margin: 16px 0 0 12px;">
                        {answers}
                    </div>

                    <p style="margin: 0; font-weight: 300; font-size: 14px;">Have a great day! See you tomorrow.</p>
                </td>
            </tr>
            <tr>
                <td bgcolor="#1b053d" style="padding: 16px 32px 16px 32px;">
                    <span style="color: white; font-weight: 300; font-size: 14px;">Want to unsubscribe? Send me a message on Twitter:</span> <a style="color: white; font-weight: 300; font-size: 14px;" href="https://twitter.com/{twitter_handle}">@{twitter_handle}</a>
                </td>
            </tr>
        </table>
    </body>
    </html>
"""

daily_answer_block = """\
    <div style="margin-bottom: 16px">
        <h6 style="margin: 0; font-weight: 400; font-size: 16px;">- {question}</h6>
        <p style="margin: 2px 0 0 12px; font-weight: 300; font-size: 14px;">{answer}</p>
    </div>
"""
def genDailyAnswerBlock(question: str, answer: str) -> str:
    return daily_answer_block.format(question=question, answer=answer)

def genDailyAnswers(name: str, answers: str) -> str:
    return daily_answers.format(subject=SUBJECT_NAME, name=name, answers=answers, twitter_handle=SUBJECT_TWITTER)