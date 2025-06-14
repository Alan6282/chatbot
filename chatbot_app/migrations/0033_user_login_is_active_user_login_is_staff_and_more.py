# Generated by Django 5.1.5 on 2025-05-05 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0032_user_login_last_login_alter_user_login_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_login',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user_login',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user_login',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user_login',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
