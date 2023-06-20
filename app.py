from flask import Flask
from routes_home import home
from routes_admin import admin, vote_create, vote_edit, vote_delete, vote_reorder, update_vote_id, clear_vote_id, user_create, user_edit, user_delete, user_reorder, user_activate, update_user_id, clear_user_id
from routes_vote import vote, search_username_in_choices
from routes_register import register
from routes_login import login
from routes_logout import logout
from routes_user import user_profile
from backup import backup_data
import json
import secrets
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Generate a random secret key
secret_key = secrets.token_hex(16)

# Print the generated secret key
print("key: {}".format(secret_key))

# Load user accounts from file
with open('user_accounts.json') as f:
    user_accounts = json.load(f)

# Load voting contents from file
with open('voting_contents.json') as f:
    voting_contents = json.load(f)

app = Flask(__name__)
app.secret_key = "aa94a4a6c7c16cc424404fb19568aa37"

# Home page
app.route('/')(home)

# Admin page
app.route('/admin', methods=['GET', 'POST'])(admin)
app.route('/vote/create', methods=['GET', 'POST'])(vote_create)
app.route('/vote/edit/<vote_id>', methods=['GET', 'POST'])(vote_edit)
app.route('/vote/delete/<vote_id>', methods=['GET', 'POST'])(vote_delete)
app.route('/vote/reorder', methods=['GET', 'POST'])(vote_reorder)
app.route('/update_vote_id', methods=['POST'])(update_vote_id)
app.route('/clear_vote_id', methods=['POST'])(clear_vote_id)

app.route('/user/create', methods=['GET', 'POST'])(user_create)
app.route('/user/edit/<user_id>', methods=['GET', 'POST'])(user_edit)
app.route('/user/delete/<user_id>', methods=['GET', 'POST'])(user_delete)
app.route('/user/reorder', methods=['GET', 'POST'])(user_reorder)
app.route('/user/activate/<user_id>', methods=['GET', 'POST'])(user_activate)
app.route('/update_user_id', methods=['POST'])(update_user_id)
app.route('/clear_user_id', methods=['POST'])(clear_user_id)

# Vote page
app.route('/vote/<vote_id>', methods=['GET','POST'])(vote)

# Register page
app.route('/register', methods=['GET','POST'])(register)

# Login page
app.route('/login', methods=['GET','POST'])(login)

# User Profile page
app.route('/user', methods=['GET','POST'])(user_profile)

# User Profile page
app.route('/logout', methods=['GET','POST'])(logout)

def format_datetime(value, format='%B %d, %Y %H:%M'):
    current_datetime = datetime.now()
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M')
    if value > current_datetime:
        return value.strftime(format)
    else:
        return '<span class="expired">{}</span>'.format(value.strftime(format))

app.jinja_env.filters['format_datetime'] = format_datetime


# Utility function to load user accounts from JSON file
def load_user_accounts():
    with open('user_accounts.json') as file:
        user_accounts = json.load(file)
    return user_accounts

def user_font_style(username):
    user_accounts = load_user_accounts()

    if not any(topic['username'] == username for topic in user_accounts):
        return 'not-found'
    else:
        user_manage = [user for user in user_accounts if user['username'] == username][0]
        if user_manage['active_status'] == 'Active':
            return 'active'
        else:
            return 'inactive'

app.jinja_env.filters['user_font_style'] = user_font_style

def mark_topic_voted(username, topic):
    is_voted, your_choice = search_username_in_choices(username,topic)
    if is_voted:
        return '✔'
    else:
        return ''

app.jinja_env.filters['mark_topic_voted'] = mark_topic_voted


if __name__ == '__main__':

    # Create a scheduler instance and schedule the backup function
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_data, 'interval', days=1, start_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    scheduler.start()

    app.run()
