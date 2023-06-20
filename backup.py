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

def backup_data():

    user_accounts = load_user_accounts()
    vote_contents = load_vote_contents()

    # Save user accounts to file
    save_user_accounts(user_accounts)

    # Save voting contents to file
    save_vote_contents(vote_contents)