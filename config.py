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
    print(theme_ids)
shifts = {0: [5, 12, "Утро"], 1: [12, 19, "День"], 2: [19, 5, "Ночь"]}
