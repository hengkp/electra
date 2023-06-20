from flask import render_template, request, redirect, url_for, session, jsonify
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

# Utility function to load user accounts from JSON file
def load_user_accounts():
    with open('user_accounts.json') as file:
        user_accounts = json.load(file)
    return user_accounts

# Utility function to save user accounts to JSON file
def save_user_accounts(user_accounts):
    with open('user_accounts.json', 'w') as file:
        json.dump(user_accounts, file)

def admin():

    user = session.get('user')
    session['vote_id'] = -1
    session['user_id'] = -1

    if user == None or user['username'] != 'admin':
        return redirect(url_for('login'))

    vote_contents = load_vote_contents()
    user_accounts = load_user_accounts()

    return render_template('admin.html', user=user, vote_contents=vote_contents, user_accounts=user_accounts)


# ####################### #
# --- VOTE MANAGEMENT --- #
# ####################### #
def vote_create():

    user = session.get('user')

    if user == None or user['username'] != 'admin':
        return redirect(url_for('login'))

    vote_contents = load_vote_contents()

    if request.method == 'POST':
        topic_name = request.form['topic_name']
        description = request.form['description']
        choices = request.form.getlist('choices[]')
        expired_date = request.form['expired_date']
        result = {}
        voters = 0
        
        # Check if the topc_name is already taken
        if any(topic['topic_name'] == topic_name for topic in vote_contents):
            return render_template('vote_create.html', user=user, message='Title already taken')

        # Check if the choice is defined
        if choices == [] or len(choices) < 2:
            return render_template('vote_create.html', user=user, message='Please define at least 2 choices')
        
        # Create result section
        for choice in choices:
            result[choice] = {} 
            result[choice]['count'] = 0
            result[choice]['voters'] = []

        # Create a new user account
        new_topic = {
            'id': len(vote_contents) + 1,
            'topic_name': topic_name,
            'description': description,
            'choices': choices,
            'expired_date': expired_date,
            'result': result,
            'voters': voters
        }
        
        print(new_topic)

        vote_contents.append(new_topic)

        # Save user accounts to file
        save_vote_contents(vote_contents)
        
        # Redirect to the login page
        return redirect(url_for('admin'))
    
    return render_template('vote_create.html', user=user)

def vote_edit(vote_id):
    vote_id = int(session['vote_id'])
    vote_contents = load_vote_contents()

    if not any(topic['id'] == vote_id for topic in vote_contents):
        return redirect(url_for('admin'))

    vote = [ topic for topic in vote_contents if topic['id'] == vote_id ][0]
    user = session.get('user')

    if user == None or user['username'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Update the vote content based on the submitted form data
        vote['topic_name'] = request.form['topic_name']
        vote['description'] = request.form['description']
        vote['expired_date'] = request.form['expired_date']
        vote['choices'] = request.form.getlist('choices[]')

        # Create result section
        vote['result'] = {}
        vote['voters'] = 0
        for choice in vote['choices']:
            vote['result'][choice] = {}
            vote['result'][choice]['count'] = 0
            vote['result'][choice]['voters'] = []
        
        # Save the updated vote contents
        save_vote_contents(vote_contents)
        
        # Redirect to a success page or perform other actions as needed
        return redirect(url_for('admin'))
        
    # Render the vote edit template with the user and vote data
    return render_template('vote_edit.html', user=user, vote=vote)

def vote_delete(vote_id):
    vote_id = int(session['vote_id'])
    vote_contents = load_vote_contents()

    if not any(topic['id'] == vote_id for topic in vote_contents):
        return redirect(url_for('admin'))

    user = session.get('user')

    if user == None or user['username'] != 'admin':
        return redirect(url_for('login'))
    
    vote_contents = [ vote for vote in vote_contents if vote['id'] != vote_id ]

    # Loop through the remaining vote contents and update their IDs
    for i, vote in enumerate(vote_contents):
        vote['id'] = i + 1

    # Save the updated vote contents
    save_vote_contents(vote_contents)

    return redirect(url_for('admin'))

def vote_reorder():
    vote_contents = load_vote_contents()

    reordered_contents = sorted(vote_contents, key=lambda x: x['expired_date'], reverse=True)

    # Loop through the remaining vote contents and update their IDs
    for i, vote in enumerate(reordered_contents):
        vote['id'] = i + 1
    
    # Save the updated vote contents
    save_vote_contents(reordered_contents)

    return redirect(url_for('admin'))

def update_vote_id():
    vote_id = request.form['vote_id']
    session['vote_id'] = vote_id
    return jsonify({'message': 'Session vote_id updated successfully'})

def clear_vote_id():
    session['vote_id'] = -1
    return jsonify({'message': 'Session vote_id cleared successfully'})


# ####################### #
# --- USER MANAGEMENT --- #
# ####################### #
def user_create():

    user = session.get('user')

    if user == None or user['username'] != 'admin':
        return redirect(url_for('login'))
    
    return redirect(url_for('register'))

def user_edit(user_id):
    user_id = int(session['user_id'])
    user_accounts = load_user_accounts()

    if not any(topic['id'] == user_id for topic in user_accounts):
        return redirect(url_for('admin'))

    user_manage = [ user for user in user_accounts if user['id'] == user_id ][0]

    user = session.get('user')
    if user == None or user['username'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        
        # Update user account with new information
        user_manage['password'] = password
        user_manage['first_name'] = first_name
        user_manage['last_name'] = last_name
        user_manage['email'] = email
        user_manage['phone'] = phone
        user_manage['gender'] = gender

        # Save user accounts to file
        save_user_accounts(user_accounts)
        
        # Redirect to the user profile page with updated information
        return redirect(url_for('admin'))
    
    return render_template('user.html', user=user, user_edit=user_manage)

def user_delete(user_id):
    user_id = int(session['user_id'])
    user_accounts = load_user_accounts()

    user = session.get('user')
    if user == None or user['username'] != 'admin':
        return redirect(url_for('login'))
    
    # Prevent Delete Admin Account
    if user['id'] == user_id:
        return redirect(url_for('admin'))

    user_accounts = [ user for user in user_accounts if user['id'] != user_id ]

    # Loop through the remaining vote contents and update their IDs
    for i, user in enumerate(user_accounts):
        user['id'] = i + 1

    # Save the updated vote contents
    save_user_accounts(user_accounts)

    return redirect(url_for('admin'))

def user_reorder():
    user_accounts = load_user_accounts()

    reordered_users = sorted(user_accounts, key=lambda x: x['username'], reverse=False)

    # Loop through the remaining vote contents and update their IDs
    for i, user in enumerate(reordered_users):
        user['id'] = i + 1
    
    # Save the updated vote contents
    save_user_accounts(reordered_users)

    return redirect(url_for('admin'))


def user_activate(user_id):
    user_id = int(session['user_id'])
    user_accounts = load_user_accounts()

    user = session.get('user')
    if user == None or user['username'] != 'admin':
        return redirect(url_for('login'))

    user_manage = [ user for user in user_accounts if user['id'] == user_id ][0]

    # Reverse change of Activate Status
    if user_manage['active_status'] == 'Active':
        user_manage['active_status'] = 'Inactive'
    else:
        user_manage['active_status'] = 'Active'
    
    # Save the updated vote contents
    save_user_accounts(user_accounts)

    return redirect(url_for('admin'))

def update_user_id():
    user_id = request.form['user_id']
    session['user_id'] = user_id
    return jsonify({'message': 'Session user_id updated successfully'})

def clear_user_id():
    session['user_id'] = -1
    return jsonify({'message': 'Session user_id cleared successfully'})