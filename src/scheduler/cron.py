from crontabs import Cron, Tab
from .jobs import SEND_EMAIL_TO_ADDRESSES, RESET_ANSWERS
    
def schedule():
    Cron().schedule(
        Tab(name="SEND_EMAILS").every(hours=24).starting_at('4/24/2020 14:30').run(SEND_EMAIL_TO_ADDRESSES),
        Tab(name="RESET_ANSWERS").every(hours=24).starting_at('4/24/2020 00:00').run(RESET_ANSWERS)
    ).go()