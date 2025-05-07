from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_convert_to_jsonfield'),
    ]

    operations = [
        # Add indexes to Sitting model foreign keys
        migrations.AlterField(
            model_name='sitting',
            name='user',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='quiz_sittings',
                to='auth.user',
                db_index=True
            ),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='quiz',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='sittings',
                to='quiz.quiz',
                db_index=True
            ),
        ),
        
        # Add indexes to Progress model foreign keys
        migrations.AlterField(
            model_name='progress',
            name='user',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='quiz_progress',
                to='auth.user',
                db_index=True
            ),
        ),
        migrations.AlterField(
            model_name='progress',
            name='quiz',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='progress',
                to='quiz.quiz',
                db_index=True
            ),
        ),
        
        # Add indexes to other frequently queried foreign keys
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='questions',
                to='quiz.quiz',
                db_index=True
            ),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='answers',
                to='quiz.question',
                db_index=True
            ),
        ),
        migrations.AlterField(
            model_name='essayanswer',
            name='sitting',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='essay_answers',
                to='quiz.sitting',
                db_index=True
            ),
        ),
        migrations.AlterField(
            model_name='essayanswer',
            name='question',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='essay_answers',
                to='quiz.question',
                db_index=True
            ),
        ),
        
        # Add index to created_at fields for chronological queries
        migrations.AlterField(
            model_name='progress',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]