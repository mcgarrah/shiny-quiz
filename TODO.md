# TODO

* ~~`requirements.txt` check versions are current~~ ✅ Updated with specific version requirements
* ~~`Procfile` is not correct~~ ✅ Fixed to use proper format: `web: gunicorn shiny_quiz.wsgi:application --log-file -`
* ~~Missing a vscode launch.json file~~ ✅ Created with multiple Django configurations
* ~~`runtime.txt` file is locked to a minor version so no security fixes~~ ✅ Updated to use `python-3.13` format
* ~~replace `runtime.txt` with the newer standard file~~ ✅
* ~~update dotenv file `.env` for secrets and environment values~~ ✅ Created `.env` and `.env.example`
* ~~fix the `README.md` file to be consistent~~ ✅ Updated with comprehensive information
* ~~check that `admin.py` register all models~~ ✅ All models are registered in their respective admin.py files
* ~~remove django-tenants but keep notes for future implementation~~ ✅ Removed from settings, models, and admin
* ~~fix django-easy-quiz integration~~ ✅ Removed django-easy-quiz due to compatibility issues and implemented our own quiz functionality with CKEditor support
* ~~implement comprehensive quiz features~~ ✅ Added all requested quiz features including:
  * ~~Question order randomization~~ ✅
  * ~~Storing quiz results under each user~~ ✅
  * ~~Previous quiz scores viewable on category page~~ ✅
  * ~~Correct answers shown after each question or at the end~~ ✅
  * ~~Incomplete quiz resumption~~ ✅
  * ~~Quiz attempt limiting~~ ✅
  * ~~Question categorization~~ ✅
  * ~~Category success rate monitoring~~ ✅
  * ~~Question explanations~~ ✅
  * ~~Pass marks~~ ✅
  * ~~Multiple question types (multiple choice, true/false, essay)~~ ✅
  * ~~Custom pass/fail messages~~ ✅
  * ~~Essay question marking system~~ ✅
* ~~convert from django-ckeditor to django-ckeditor-5~~ ✅ Updated models, settings, and URLs to use the modern CKEditor 5
* Add the /about and /contact back to the top level template.
* Fix the "home" or / to stop it from HTTP 500 under gunicorn


## Additional Tasks

* evaluate [`django-tinymce`](https://github.com/jazzband/django-tinymce) as replacement for `django-ckeditor-5` due to GPL2 licence issues
* Fix the AllAuth login screens to be pretty with `django-allauth-ui`
* Add multi-tenancy support in the future:
  * Evaluate `django-tenants` vs `django-easy-tenants>=0.9.2`
  * Implement PostgreSQL database when adding multi-tenancy
  * Create tenant models (Client, Domain)
  * Configure tenant middleware and database routers
* Add unit tests for models and views
* Create fixtures for sample quiz data
* Add CI/CD pipeline configuration
* Create custom error pages (404, 500)
* Add email verification workflow
* Create documentation for API endpoints (if applicable)
* Implement HTMX for more interactive quiz experience
* Add quiz import/export functionality
* Implement quiz sharing via social media
* Add quiz leaderboards
* Add the `django-debug-toolbar`

## Areas for Improvement

* Testing: No test files were found in the review. Add comprehensive tests: Implement unit and integration tests for models, views, and forms.
``` text
# Add to requirements.txt
pytest>=7.3.1
pytest-django>=4.5.2
factory-boy>=3.2.1
coverage>=7.2.5
```
* License considerations: Address license concerns: Evaluate `django-tinymce` as mentioned in the TODO to avoid GPL2 license issues.
* Multi-tenancy: Currently removed but planned for future implementation. This would be a significant architectural change.
* UI enhancements:
  * Enhance UI/UX: Complete the AllAuth UI improvements for a more consistent user experience improving AllAuth login screens with `django-allauth-ui`.
  * Interactive features: Adding HTMX for more interactive quiz experiences is mentioned in the TODO list.
* Social features: Add the planned Quiz sharing and leaderboards but not yet implemented.
* Consider performance optimizations: As the application grows, database query optimization might be needed, especially for quiz results and progress tracking.
* Set up CI/CD: Implement continuous integration and deployment pipelines as mentioned in the TODO.
* Complete documentation: Add API documentation if applicable and more detailed developer guides.
* Add REST API Endpoints with Django REST Framework using `djangorestframework` which enables:
  * Modile app integration
  * Third-party integrations
  * HTMX interactions for more dynamic UI
* Quiz Analytics and Reporting via a dashboard with:
  * Quiz completion rates
  * Average scores by category
  * Time spent on questions
  * Most challenging questions
  * User performance trends
* Add support for Advanced Question Types such as:
  * Matching questions
  * Drag-and-drop ordering
  * Code execution questions
  * Image-based questions
  * Audio/video questions
* Ensure the application is fully accessible:
  * ARIA attributes
  * Keyboard navigation
  * Screen reader compatibility
  * High contrast mode
  * Font size adjustments


## Code Cleanup Opportunities

1. ~~Data Storage in Text Fields~~ ✅ Replaced text fields with JSONField

  ~~Issue: The Sitting model uses comma-separated text fields to store question IDs and user answers.~~
  ~~Recommendation: Replace with proper relational models or use Django's JSONField, which would eliminate the need for string parsing and improve data integrity.~~

2. ~~Inefficient Database Queries~~ ✅ Optimized with select_related and prefetch_related

  ~~Issue: In category_detail view, there's a loop with database queries~~
  ~~Recommendation: Use prefetch_related or select_related to reduce database hits~~

3. ~~JSONField Implementation Issues~~ ✅ Fixed with improved error handling and database-agnostic migrations

  ~~Issue: The migration strategy for JSONField used direct SQL, and there was limited error handling for JSONField access~~
  ~~Recommendation: Use database-agnostic migrations and add defensive programming for JSONField access~~

4. Dark mode does show the text on the tiles for the Quizzes, Categories and other places. The text is too dark.

5. ~~Missing Index on Foreign Keys~~ ✅ Added indexes to all foreign keys and frequently queried fields

  ~~Issue: High-traffic tables like Progress and Sitting don't have explicit database indexes on foreign keys.~~
  ~~Recommendation: Add indexes to improve query performance~~

6. ~~Potential Race Conditions~~ ✅ Fixed with transactions and F() expressions
 
  ~~Issue: The add_user_answer method in the Sitting model updates fields and then saves, which could lead to race conditions in concurrent environments.~~
  ~~Recommendation: Use F() expressions or transactions~~

7. ~~Missing Pagination in API Views~~ ✅ Added consistent pagination to all list views

  ~~Issue: Some views that could return large datasets (like quiz_list) implement pagination, but others don't.~~
  ~~Recommendation: Consistently apply pagination to all list views that could grow large.~~

8. Inconsistent Error Handling

  Issue: Error handling is inconsistent across views. Some use messages.error() while others just redirect.
  Recommendation: Standardize error handling approach across all views.

9. Missing Form Validation

  Issue: Some views process form data directly from request.POST without proper validation.
  Recommendation: Use Django forms for all data processing to ensure proper validation.

10. Missing Cache Implementation

  Issue: No caching strategy is implemented, which could impact performance for frequently accessed data.
  Recommendation: Add Django's caching framework for views like category listings and quiz details.

11. Missing Documentation

  Issue: Code documentation is minimal, making it harder for new developers to understand the codebase.
  Recommendation: Add docstrings to all models, views, and complex methods explaining their purpose and usage.

12. Potential Timezone Issues

  Issue: Time-related calculations (like quiz time limits) don't explicitly handle timezone differences.
  Recommendation: Ensure all datetime operations use Django's timezone-aware functions consistently.

13. Redundant Database Queries

  Issue: Despite optimizations, there are still some views that could benefit from further query reduction.
  Recommendation: Use Django Debug Toolbar to identify remaining N+1 query issues and optimize them.
