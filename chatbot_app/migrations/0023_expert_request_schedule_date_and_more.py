# Generated by Django 5.1.5 on 2025-03-11 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0022_alter_user_det_login_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert_request',
            name='schedule_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='expert_request',
            name='schedule_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='expert_request',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
