# Generated by Django 5.1.5 on 2025-03-15 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0024_alter_expert_det_login_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert_request',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
