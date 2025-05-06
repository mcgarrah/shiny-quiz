#!/usr/bin/env python
"""
Script to set up sample data for the Shiny Quiz application.
This script will:
1. Generate proper password hashes for the sample users
2. Load all fixture data
"""
import os
import sys
import subprocess
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shiny_quiz.settings')
django.setup()

# Import the password hash generation function
from generate_password_hashes import update_fixture_file

def main():
    """Main function to set up sample data"""
    print("Setting up sample data for Shiny Quiz...")
    
    # Step 1: Generate password hashes
    print("\n=== Step 1: Generating password hashes ===")
    success = update_fixture_file()
    if not success:
        print("Failed to update password hashes. Aborting.")
        return False
    
    # Step 2: Load fixture data
    print("\n=== Step 2: Loading fixture data ===")
    fixtures = [
        'fixtures/01_users.json',
        'fixtures/02_user_profiles.json',
        'fixtures/03_categories.json',
        'fixtures/04_quizzes.json',
        'fixtures/05_questions_python.json',
        'fixtures/06_questions_physics.json',
        'fixtures/07_questions_algebra.json',
        'fixtures/08_questions_history.json',
        'fixtures/09_questions_general.json',
        'fixtures/10_progress.json'
    ]
    
    # Build the command
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manage_py = os.path.join(base_dir, 'manage.py')
    command = [sys.executable, manage_py, 'loaddata'] + fixtures
    
    # Execute the command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        print("\nFixture data loaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error loading fixture data: {e}")
        print(e.stderr)
        return False
    
    print("\n=== Sample data setup complete! ===")
    print("\nYou can now log in with the following credentials:")
    print("  admin / admin")
    print("  teacher / teacher")
    print("  student / student")
    
    return True

if __name__ == '__main__':
    main()