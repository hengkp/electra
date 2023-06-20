from flask import render_template, request, redirect, url_for, session
import json

# Utility function to load user accounts from JSON file
def load_user_accounts():
    with open('user_accounts.json') as file:
        user_accounts = json.load(file)
    return user_accounts

def login():
    if request.method == 'POST':
        # Handle form submission
        username = request.form.get('username')
        password = request.form.get('password')

        # Perform login authentication
        user = authenticate(username, password)
        session['user'] = user
        if user:
            # Set user information in session
            return redirect(url_for('home'))
        else:
            # Invalid credentials, show error message
            error_message = 'Invalid username or password'
            return render_template('login.html', message=error_message)

    # GET request - display the login form
    return render_template('login.html')

# Helper function to authenticate user
def authenticate(username, password):
    
    user_accounts = load_user_accounts()

    for user in user_accounts:
        if user['username'] == username and user['password'] == password:
            return user

    return None
