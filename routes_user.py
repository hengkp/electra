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

def user_profile():
    user = session['user']
    user_accounts = load_user_accounts()
    
    if request.method == 'POST':
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        
        # Update user account with new information
        user['password'] = password
        user['first_name'] = first_name
        user['last_name'] = last_name
        user['email'] = email
        user['phone'] = phone
        user['gender'] = gender

        # Save user accounts to file
        save_user_accounts(user_accounts)
        
        # Redirect to the user profile page with updated information
        return redirect(url_for('home'))
    
    return render_template('user.html', user=user, user_edit=user)
