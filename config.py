from dotenv import load_dotenv
import json
import os
from shifts.shifts import get_current_working_shift

load_dotenv()

token = os.getenv('BOT_TOKEN')
theme_ids = {}
admin_users = []
thread_config = os.getenv("THREAD_IDS")
current_shift = '4'
if thread_config:
    theme_ids = json.loads(thread_config)
for user_id in os.getenv("ADMIN_USERS").split(', '):
    admin_users.append(int(user_id))
shifts = {0: [4, 11, "Утро"], 1: [11, 18, "День"], 2: [18, 4, "Ночь"]}
print(get_current_working_shift())
