from dotenv import load_dotenv
import json
import os
from shifts.shifts import get_current_working_shift

load_dotenv()

token = os.getenv('BOT_TOKEN')
theme_ids = {}
admin_users = []
thread_config = os.getenv("THREAD_IDS")
if thread_config:
    theme_ids = json.loads(thread_config)
for user_id in os.getenv("ADMIN_USERS").split(', '):
    admin_users.append(int(user_id))
shifts = {0: [4, 11, "Утро"], 1: [11, 18, "День"], 2: [18, 4, "Ночь"]}
shift_to_chat = dict()
for k in theme_ids.keys():
    shift_to_chat[k] = theme_ids[k][0]

chat_to_thread = dict()
for k in theme_ids.keys():
    chat_to_thread[theme_ids[k][0]] = theme_ids[k][1]

chat_to_shift = dict()
for k in theme_ids.keys():
    chat_to_shift[theme_ids[k][0]] = k

print(get_current_working_shift())

