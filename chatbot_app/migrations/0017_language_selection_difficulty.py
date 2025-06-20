# Generated by Django 5.1.5 on 2025-03-04 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0016_alter_assessmentquestion_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='language_selection',
            name='difficulty',
            field=models.CharField(choices=[('A1', 'Beginner'), ('A2', 'Elementary'), ('B1', 'Intermediate'), ('B2', 'Upper Intermediate'), ('C1', 'Advanced'), ('C2', 'Mastery')], default='A1', max_length=2),
            preserve_default=False,
        ),
    ]
