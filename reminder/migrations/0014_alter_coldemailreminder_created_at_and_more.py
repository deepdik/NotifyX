# Generated by Django 4.0 on 2024-10-22 18:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0013_alter_coldemailreminder_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coldemailreminder',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='coldemailreminder',
            name='failure_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coldemailreminder',
            name='reminder_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coldemailreminder',
            name='reminder_failure_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coldemailreminder',
            name='sent_count',
            field=models.IntegerField(default=0),
        ),
    ]
