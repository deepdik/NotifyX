# Generated by Django 4.0 on 2024-10-23 00:27

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0015_coldemaillog_deactivate_coldemailreminder_deactivate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coldemailreminder',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text="Enter the email body using Markdown. Leave blank if you're using plain text."),
        ),
        migrations.AlterField(
            model_name='coldemailreminder',
            name='reminder_template',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text="Enter the Markdown reminder email template. Leave blank if you're using plain text for reminders."),
        ),
        migrations.AlterField(
            model_name='personalemailreminder',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]