# Sample Data Fixtures

This directory contains sample data fixtures for the Shiny Quiz application. These fixtures can be loaded using Django's `loaddata` management command to populate the database with sample data for testing and development purposes.

## Available Fixtures

1. **01_users.json** - Sample user accounts
   - admin (superuser)
   - teacher (staff user)
   - student (regular user)

2. **02_user_profiles.json** - User profiles for the sample users

3. **03_categories.json** - Quiz categories
   - Programming
   - Science
   - Mathematics
   - History
   - General Knowledge

4. **04_quizzes.json** - Sample quizzes with different settings
   - Python Basics
   - Basic Physics
   - Algebra Fundamentals
   - World War II
   - General Knowledge Challenge

5. **05_questions_python.json** - Questions for the Python Basics quiz
6. **06_questions_physics.json** - Questions for the Basic Physics quiz
7. **07_questions_algebra.json** - Questions for the Algebra Fundamentals quiz
8. **08_questions_history.json** - Questions for the World War II quiz
9. **09_questions_general.json** - Questions for the General Knowledge Challenge quiz

10. **10_progress.json** - Sample progress data for the student user

## Loading the Fixtures

### Option 1: Using the Setup Script (Recommended)

The easiest way to load all the sample data is to use the setup script, which will generate proper password hashes and load all fixtures:

```bash
python scripts/setup_sample_data.py
```

### Option 2: Using VSCode Launch Configurations

You can use the VSCode launch configurations to load the fixtures:

1. First run "Python: Generate Password Hashes" to update the password hashes
2. Then run "Python: Django LoadData" to load all fixtures

Or use the combined configuration:
- "Python: Setup Sample Data (Generate Hashes + Load All)"

### Option 3: Manual Process

1. Generate proper password hashes:
   ```bash
   python scripts/generate_password_hashes.py --update
   ```

2. Load all fixtures at once:
   ```bash
   python manage.py loaddata fixtures/01_users.json fixtures/02_user_profiles.json fixtures/03_categories.json fixtures/04_quizzes.json fixtures/05_questions_python.json fixtures/06_questions_physics.json fixtures/07_questions_algebra.json fixtures/08_questions_history.json fixtures/09_questions_general.json fixtures/10_progress.json
   ```

3. Or load them individually in the correct order:
   ```bash
   python manage.py loaddata fixtures/01_users.json
   python manage.py loaddata fixtures/02_user_profiles.json
   python manage.py loaddata fixtures/03_categories.json
   python manage.py loaddata fixtures/04_quizzes.json
   python manage.py loaddata fixtures/05_questions_python.json
   python manage.py loaddata fixtures/06_questions_physics.json
   python manage.py loaddata fixtures/07_questions_algebra.json
   python manage.py loaddata fixtures/08_questions_history.json
   python manage.py loaddata fixtures/09_questions_general.json
   python manage.py loaddata fixtures/10_progress.json
   ```

## User Credentials

After loading the fixtures and running the password hash generation script, the sample users will have the following credentials:

- **admin** / admin (superuser with full access)
- **teacher** / teacher (staff user who can create and manage quizzes)
- **student** / student (regular user who can take quizzes)

**Note:** These are insecure passwords intended only for development. In a production environment, you should use strong, unique passwords for all accounts.