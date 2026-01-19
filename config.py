from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv('BOT_TOKEN')
theme_ids = []
admin_users = []
for user_id in os.getenv("ADMIN_USERS").split(', '):
    admin_users.append(int(user_id))
for theme_id in os.getenv('THREAD_IDS').split(', '):
    theme_ids.append(int(theme_id))
shifts = {0: [4, 11, "Утро"], 1: [11, 18, "День"], 2: [18, 4, "Ночь"]}
