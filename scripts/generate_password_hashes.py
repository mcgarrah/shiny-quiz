#!/usr/bin/env python
"""
Script to generate proper password hashes for Django users.
This can be used to update the fixture files with valid password hashes.
"""
import os
import sys
import json
import django
from django.contrib.auth.hashers import make_password

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shiny_quiz.settings')
django.setup()

# User credentials to generate hashes for
USERS = [
    {'username': 'admin', 'password': 'admin'},
    {'username': 'teacher', 'password': 'teacher'},
    {'username': 'student', 'password': 'student'},
]

def generate_password_hashes():
    """Generate password hashes for the sample users"""
    print("Generating password hashes for sample users...")
    
    for user in USERS:
        username = user['username']
        password = user['password']
        hashed_password = make_password(password)
        
        print(f"User: {username}")
        print(f"Password: {password}")
        print(f"Hashed password: {hashed_password}")
        print("-" * 50)

def update_fixture_file():
    """Update the users fixture file with proper password hashes"""
    fixture_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               'fixtures', '01_users.json')
    
    try:
        with open(fixture_path, 'r') as f:
            users_data = json.load(f)
        
        # Update password hashes
        for i, user in enumerate(USERS):
            if i < len(users_data):
                users_data[i]['fields']['password'] = make_password(user['password'])
        
        # Write updated data back to file
        with open(fixture_path, 'w') as f:
            json.dump(users_data, f, indent=2)
        
        print(f"Updated password hashes in {fixture_path}")
        return True
    except Exception as e:
        print(f"Error updating fixture file: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--update':
        update_fixture_file()
    else:
        generate_password_hashes()
        print("\nTo update the fixture file with these hashes, run:")
        print("python scripts/generate_password_hashes.py --update")