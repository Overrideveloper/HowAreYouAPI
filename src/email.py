from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from src.constants import SENDGRID_KEY, SENDER_EMAIL

def createMail(recipient: str, subject: str, content: str, html: bool = True):
    if html:
        return Mail(from_email=SENDER_EMAIL, to_emails=recipient, subject=subject, html_content=content)
    else:
        return Mail(from_email=SENDER_EMAIL, to_emails=recipient, subject=subject, plain_text_content=content)
    
def sendMail(mail: Mail):
    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        sg.send(mail)
        
        return True
    except:
        return False
