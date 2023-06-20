from flask import redirect, url_for, session

def logout():
    if 'user' in session:
        # Clear the session data
        session.pop('user', None)
    return redirect(url_for('home'))