# Generated by Django 5.1.5 on 2025-03-04 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0018_alter_language_selection_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='language_selection',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]
