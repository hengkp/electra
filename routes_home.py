from flask import render_template, session
import json

# Utility function to load vote contents from JSON file
def load_vote_contents():
    with open('voting_contents.json') as file:
        vote_contents = json.load(file)
    return vote_contents

# Utility function to save vote contents to JSON file
def save_vote_contents(vote_contents):
    with open('voting_contents.json', 'w') as file:
        json.dump(vote_contents, file)

def home():
    
    vote_contents = load_vote_contents()

    # Check if user is logged in
    user = session.get('user')
    if user:
        if user['active_status'] == 'Active':
            return render_template('home.html', user=user, active_votes=vote_contents)
        else:
            return render_template('home.html', message="Your account has suspened. Please contact administrator for help.")
    else:
        return render_template('home.html')
