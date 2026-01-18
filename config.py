from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv('BOT_TOKEN')
theme_id = os.getenv('THEME_ID')
admin_users = []
for user_id in os.getenv("ADMIN_USERS").split(', '):
    admin_users.append(int(user_id))
shifts = {0: [5, 12, "Утро"], 1: [12, 19, "День"], 2: [19, 5, "Ночь"]}
