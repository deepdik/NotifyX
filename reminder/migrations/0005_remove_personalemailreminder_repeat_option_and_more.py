# Generated by Django 4.0 on 2024-10-21 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0004_coldemailreminder_reminder_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalemailreminder',
            name='repeat_option',
        ),
        migrations.AddField(
            model_name='personalemailreminder',
            name='scheduled_time_of_day',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personalemailreminder',
            name='scheduled_day_of_week',
            field=models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday'), ('All days', 'All days')], max_length=10, null=True),
        ),
    ]