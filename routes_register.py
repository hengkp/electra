from flask import render_template, redirect, request, url_for, session
import json


# Utility function to load user accounts from JSON file
def load_user_accounts():
    with open('user_accounts.json') as file:
        user_accounts = json.load(file)
    return user_accounts

# Utility function to save user accounts to JSON file
def save_user_accounts(user_accounts):
    with open('user_accounts.json', 'w') as file:
        json.dump(user_accounts, file)

def register():

    user_accounts = load_user_accounts()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        
        # Check if the username is already taken
        if any(account['username'] == username for account in user_accounts):
            return render_template('register.html', message='Username already taken')
        
        # Create a new user account
        new_account = {
            'id': len(user_accounts) + 1,
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'gender': gender,
            'active_status': 'Active'
        }
        
        user_accounts.append(new_account)

        # Save user accounts to file
        save_user_accounts(user_accounts)

        session['user'] = new_account
        
        # Redirect to the login page
        return redirect(url_for('home'))
    
    return render_template('register.html')
