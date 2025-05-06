# Shiny Quiz Setup Guide

This guide will help you set up and run the Shiny Quiz application.

## Prerequisites

- Python 3.13.x
- pip (Python package manager)
- Git

## Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/mcgarrah/shiny-quiz.git
   cd shiny-quiz
   ```

2. **Create and activate a virtual environment**

   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the application**

   Open your browser and navigate to http://127.0.0.1:8000/

## Setting Up Social Authentication

### Google OAuth

1. Go to the [Google Developer Console](https://console.developers.google.com/)
2. Create a new project
3. Enable the Google+ API
4. Create OAuth 2.0 credentials
5. Add your domain to authorized domains
6. Add your callback URL: `http://localhost:8000/accounts/google/login/callback/`
7. Update your `.env` file with the client ID and secret

### Facebook OAuth

1. Go to the [Facebook Developer Portal](https://developers.facebook.com/)
2. Create a new app
3. Set up Facebook Login
4. Add your callback URL: `http://localhost:8000/accounts/facebook/login/callback/`
5. Update your `.env` file with the app ID and secret

## Future Multi-tenancy Support

Multi-tenancy support is planned for future implementation. When ready to implement:

1. Choose between django-tenants or django-easy-tenants
2. Switch from SQLite to PostgreSQL
3. Update settings.py with tenant configuration
4. Create tenant models
5. Configure middleware and database routers

## Troubleshooting

- **Database connection issues**: Ensure your database settings in `.env` are correct
- **Static files not loading**: Run `python manage.py collectstatic`
- **Migration errors**: Try `python manage.py makemigrations` before migrating