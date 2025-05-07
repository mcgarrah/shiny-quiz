from django.db import migrations, models
from django.db.models import JSONField

def convert_text_to_json(apps, schema_editor):
    Sitting = apps.get_model('quiz', 'Sitting')
    for sitting in Sitting.objects.all():
        # Convert question_list from comma-separated string to list
        if sitting.question_list:
            try:
                sitting.question_list_json = [int(q_id) for q_id in sitting.question_list.split(',') if q_id]
            except (ValueError, TypeError):
                sitting.question_list_json = []
        else:
            sitting.question_list_json = []
            
        # Convert question_order from comma-separated string to list
        if sitting.question_order:
            try:
                sitting.question_order_json = [int(q_id) for q_id in sitting.question_order.split(',') if q_id]
            except (ValueError, TypeError):
                sitting.question_order_json = []
        else:
            sitting.question_order_json = []
            
        # Convert incorrect_questions from comma-separated string to list
        if sitting.incorrect_questions:
            try:
                sitting.incorrect_questions_json = [int(q_id) for q_id in sitting.incorrect_questions.split(',') if q_id]
            except (ValueError, TypeError):
                sitting.incorrect_questions_json = []
        else:
            sitting.incorrect_questions_json = []
            
        # Convert user_answers from comma-separated string to dict
        user_answers_dict = {}
        if sitting.user_answers:
            try:
                for answer in sitting.user_answers.split(','):
                    if not answer:
                        continue
                    
                    parts = answer.split(':')
                    if len(parts) != 2:
                        continue
                        
                    question_id, answer_id = parts
                    if answer_id:
                        try:
                            user_answers_dict[str(question_id)] = int(answer_id)
                        except ValueError:
                            user_answers_dict[str(question_id)] = None
                    else:
                        user_answers_dict[str(question_id)] = None
            except Exception:
                # If any error occurs, use an empty dict
                user_answers_dict = {}
        
        sitting.user_answers_json = user_answers_dict
        sitting.save()

def copy_json_data(apps, schema_editor):
    """
    Copy data from temporary JSON fields to the final fields
    using Django's ORM for database agnosticism
    """
    Sitting = apps.get_model('quiz', 'Sitting')
    for sitting in Sitting.objects.all():
        sitting.question_list = sitting.question_list_json
        sitting.question_order = sitting.question_order_json
        sitting.incorrect_questions = sitting.incorrect_questions_json
        sitting.user_answers = sitting.user_answers_json
        sitting.save()

def convert_json_to_text(apps, schema_editor):
    Sitting = apps.get_model('quiz', 'Sitting')
    for sitting in Sitting.objects.all():
        # Convert question_list from list to comma-separated string
        sitting.question_list = ','.join(str(q_id) for q_id in sitting.question_list_json)
        
        # Convert question_order from list to comma-separated string
        sitting.question_order = ','.join(str(q_id) for q_id in sitting.question_order_json)
        
        # Convert incorrect_questions from list to comma-separated string
        sitting.incorrect_questions = ','.join(str(q_id) for q_id in sitting.incorrect_questions_json)
        
        # Convert user_answers from dict to comma-separated string
        user_answers_str = ''
        for question_id, answer_id in sitting.user_answers_json.items():
            if answer_id is not None:
                user_answers_str += f"{question_id}:{answer_id},"
            else:
                user_answers_str += f"{question_id}:,"
        
        sitting.user_answers = user_answers_str
        sitting.save()

class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        # Add temporary JSON fields
        migrations.AddField(
            model_name='sitting',
            name='question_list_json',
            field=JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sitting',
            name='question_order_json',
            field=JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sitting',
            name='incorrect_questions_json',
            field=JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sitting',
            name='user_answers_json',
            field=JSONField(default=dict),
        ),
        
        # Convert data from text fields to JSON fields
        migrations.RunPython(convert_text_to_json, convert_json_to_text),
        
        # Remove old text fields
        migrations.RemoveField(
            model_name='sitting',
            name='question_list',
        ),
        migrations.RemoveField(
            model_name='sitting',
            name='question_order',
        ),
        migrations.RemoveField(
            model_name='sitting',
            name='incorrect_questions',
        ),
        migrations.RemoveField(
            model_name='sitting',
            name='user_answers',
        ),
        
        # Add new JSON fields with original names
        migrations.AddField(
            model_name='sitting',
            name='question_list',
            field=JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sitting',
            name='question_order',
            field=JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sitting',
            name='incorrect_questions',
            field=JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sitting',
            name='user_answers',
            field=JSONField(default=dict),
        ),
        
        # Copy data from temporary fields to new fields using Django ORM
        migrations.RunPython(
            code=copy_json_data,
            reverse_code=lambda apps, schema_editor: None
        ),
        
        # Remove temporary fields
        migrations.RemoveField(
            model_name='sitting',
            name='question_list_json',
        ),
        migrations.RemoveField(
            model_name='sitting',
            name='question_order_json',
        ),
        migrations.RemoveField(
            model_name='sitting',
            name='incorrect_questions_json',
        ),
        migrations.RemoveField(
            model_name='sitting',
            name='user_answers_json',
        ),
    ]