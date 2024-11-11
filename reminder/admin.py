from django.contrib import admin
from .models import ColdEmailReminder, ColdEmailLog, PersonalEmailReminder, PersonalEmailLog
from markdownx.admin import MarkdownxModelAdmin


# Registering ColdEmailReminder
@admin.register(ColdEmailReminder)
class ColdEmailReminderAdmin(MarkdownxModelAdmin):
    list_display = (
        'subject', 'recipients', 'scheduled_time', 'reminder_frequency', 'max_reminders', 'sent_count', 'failure_count',
        'created_at', 'reminder_count')
    search_fields = ('subject', 'recipients')
    list_filter = ('reminder_frequency', 'created_at')
    readonly_fields = ('sent_count', 'failure_count', 'created_at', 'reminder_count')
    fields = (
        'recipients', 'subject', 'body', 'reminder_template', 'instant_send', 'scheduled_time', 'reminder_frequency',
        'reminder_time', 'max_reminders', 'sent_count', 'failure_count', 'created_at', 'reminder_count', 'deactivate')


# Registering ColdEmailLog
@admin.register(ColdEmailLog)
class ColdEmailLogAdmin(admin.ModelAdmin):
    list_display = ('email_reminder', 'sent_date', 'sent_time')
    search_fields = ('email_reminder__subject', 'sent_date')
    list_filter = ('sent_date',)


# Registering PersonalEmailReminder
@admin.register(PersonalEmailReminder)
class PersonalEmailReminderAdmin(MarkdownxModelAdmin):
    list_display = (
        'subject', 'recipient', 'scheduled_time', 'scheduled_day_of_week', 'scheduled_time_of_day', 'sent_count',
        'failure_count', 'created_at')
    search_fields = ('subject', 'recipient')
    list_filter = ('scheduled_day_of_week', 'created_at')
    readonly_fields = ('sent_count', 'failure_count', 'created_at')
    fields = (
        'recipient', 'subject', 'body', 'scheduled_time', 'scheduled_day_of_week', 'scheduled_time_of_day',
        'sent_count',
        'failure_count', 'created_at', 'deactivate')


# Registering PersonalEmailLog
@admin.register(PersonalEmailLog)
class PersonalEmailLogAdmin(admin.ModelAdmin):
    list_display = ('email_reminder', 'sent_date', 'sent_time')
    search_fields = ('email_reminder__subject', 'sent_date')
    list_filter = ('sent_date',)
