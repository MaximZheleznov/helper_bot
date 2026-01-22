from dotenv import load_dotenv
import json
import os


load_dotenv()

token = os.getenv('BOT_TOKEN')
theme_ids = {}
admin_users = []
thread_config = os.getenv("THREAD_IDS")
if thread_config:
    theme_ids = json.loads(thread_config)
for user_id in os.getenv("ADMIN_USERS").split(', '):
    admin_users.append(int(user_id))

