# Scripts Directory

This directory contains utility scripts for the Shiny Quiz Django application.

## Scripts

### generate_password_hashes.py
Generates proper Django password hashes for sample user data.

**Usage:**
```bash
python scripts/generate_password_hashes.py --update
```

**Purpose:**
- Updates fixture files with properly hashed passwords
- Required before loading sample user data
- Ensures secure password storage in fixtures

### pin_requirements.py
Manages requirement version pinning for security auditing.

**Usage:**
```bash
# Pin requirements to exact minimum versions
python scripts/pin_requirements.py pin

# Unpin requirements back to flexible versions
python scripts/pin_requirements.py unpin
```

**Purpose:**
- Pin mode: Converts `>=` to `==` using minimum versions, creates `requirements-pinned.txt`
- Unpin mode: Converts `==` back to `>=` in requirements.txt
- Enables security auditing with exact versions

### setup_sample_data.py
One-click setup for sample data including users, quizzes, and questions.

**Usage:**
```bash
python scripts/setup_sample_data.py
```

**Purpose:**
- Generates password hashes and loads all fixture data
- Creates sample users (admin/admin, teacher/teacher, student/student)
- Loads 5 quiz categories, 5 quizzes, and 25 questions
- Sets up sample progress data

## Requirements

All scripts should be run from the project root directory with the virtual environment activated:

```bash
source .venv/bin/activate
python scripts/[script_name].py
```