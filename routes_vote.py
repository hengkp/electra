from flask import render_template, redirect, request, url_for, session #, flash
from datetime import datetime
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

def search_username_in_choices(username, topic):
    for choice in topic['result']:
        voters = topic['result'][choice]['voters']
        if username in voters:
            return True, choice
    return False, None

def vote(vote_id):

    user = session.get('user')
    vote_contents = load_vote_contents()

    if user == None:
        return redirect(url_for('login'))

    topic = next((content for content in vote_contents if content.get('id') == int(vote_id)), None)

    if topic:

        # Calculate remaining time
        expired_date = datetime.strptime(topic['expired_date'], '%Y-%m-%dT%H:%M') # format = '%Y-%m-%d %H:%M:%S'
        current_time = datetime.now()
        time_remaining = expired_date - current_time

        # Check if the time has expired
        if time_remaining.total_seconds() <= 0:
            time_remaining = 0

        # Calculate max_voters for result
        max_voters = 0
        vote_rank = sorted(topic['choices'], key=lambda choice: topic['result'][choice]['count'], reverse=True)
        if time_remaining == 0:
            for choice in topic['choices']:
                voters_count = int(topic['result'][choice]['count'])
                if voters_count > max_voters:
                    max_voters = voters_count

        if request.method == 'POST':

            is_voted, your_choice = search_username_in_choices(user['username'],topic)

            if not is_voted:
                choice = request.form['choice']
                topic['result'][choice]['count'] += 1
                topic['result'][choice]['voters'].append(user['username'])
                topic['voters'] += 1
                save_vote_contents(vote_contents)
                return render_template('vote_success.html', user=user)

            else:
                return render_template('vote.html',user=user, vote=topic, message='You have voted for "{}" .'.format(your_choice), time_remaining=time_remaining, max_voters=max_voters, vote_rank=vote_rank)

    return render_template('vote.html',user=user, vote=topic, time_remaining=time_remaining, max_voters=max_voters, vote_rank=vote_rank)