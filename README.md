# Shiny Quiz

Shiny Quiz Web App using Django 5.2

My goal is to build a **Shiny New Quiz Web App** using Django with its very opinionated framework to accelerate the development. I have built the [Legendary Quick Quiz](https://github.com/mcgarrah/legendary_quick_quiz) using the Python Flask framework as an exercise to refresh my skills in that framework.

## Technical Requirements

* Django 5.2
* Bootstrap 5 for modern UI with light/dark mode support
* Python 3.13.x runtime
* Easy managed deployment with `Procfile`, `runtime.txt`
* SQLite3 for initial development (with plans for PostgreSQL support in the future)
* Social media login via django-allauth and django-allauth-ui
* Rich text editing via django-ckeditor-5

## Features

* User authentication with social login options
* Quiz creation and management with multiple question types (multiple choice, true/false, essay)
* Question order randomization
* Timed quizzes with automatic submission
* Results tracking and statistics
* Responsive design with light/dark mode
* Admin interface for content management
* Progress tracking by category
* Essay question marking system
* Pass/fail messaging
* Single attempt restriction option
* Explanation for each question

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/mcgarrah/shiny-quiz.git
   cd shiny-quiz
   ```

2. Create a virtual environment and install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. (Optional) Load sample data:
   ```
   # Option 1: Use the setup script (recommended)
   python scripts/setup_sample_data.py
   
   # Option 2: Manual process
   # First, generate proper password hashes
   python scripts/generate_password_hashes.py --update
   
   # Then load the fixtures
   python manage.py loaddata fixtures/01_users.json fixtures/02_user_profiles.json fixtures/03_categories.json fixtures/04_quizzes.json fixtures/05_questions_python.json fixtures/06_questions_physics.json fixtures/07_questions_algebra.json fixtures/08_questions_history.json fixtures/09_questions_general.json fixtures/10_progress.json
   ```

   Alternatively, you can use the VSCode launch configurations:
   - "Python: Setup Sample Data (Generate Hashes + Load All)" - One-click setup
   - "Python: Generate Password Hashes" followed by "Python: Django LoadData" - Two-step process

7. Run the development server:
   ```
   python manage.py runserver
   ```

## Sample Data

The application comes with sample data that can be loaded using the Django `loaddata` command. This includes:

- 3 user accounts (admin, teacher, student)
- 5 quiz categories (Programming, Science, Mathematics, History, General Knowledge)
- 5 quizzes with different settings
- 25 questions across all quizzes (multiple choice, true/false, and essay)
- Sample progress data for the student user

After loading the data, the sample users will have the following credentials:
- admin / admin
- teacher / teacher
- student / student

(You should change these passwords in a production environment)

## References

* [Configurable quiz app for Django](https://github.com/tomwalker/django_quiz) that is over 7 years old but has great requirements list
* [Django app for quizzes for Azure](https://github.com/pamelafox/django-quiz-app) that is more recent and worth reviewing
* [Create a quiz app with HTMX and Django in 8 mins](https://tomdekan.com/articles/quiz-htmx) by Tom Dekan Published: March 5, 2024