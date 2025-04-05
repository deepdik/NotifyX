from django.contrib import admin
from .models import (
    ColdEmailReminder,
    ColdEmailLog,
    PersonalEmailReminder,
    PersonalEmailLog,
    MessageTemplate,
    SubjectTemplate, Resume
)
from markdownx.admin import MarkdownxModelAdmin


# ColdEmailReminder Admin
@admin.register(ColdEmailReminder)
class ColdEmailReminderAdmin(MarkdownxModelAdmin):
    list_display = (
        'display_subject', 'recipients', 'scheduled_time', 'reminder_frequency',
        'max_reminders', 'sent_count', 'failure_count', 'created_at',
        'reminder_count'
    )
    search_fields = ('subject', 'recipients')
    list_filter = ('reminder_frequency', 'created_at')
    readonly_fields = ('sent_count', 'failure_count', 'created_at', 'reminder_count')
    fields = (
        'recipients', 'subject', 'subject_template', 'body', 'main_message_template',
        'reminder_template', 'reminder_message_template',
        'instant_send', 'scheduled_time', 'reminder_frequency', 'reminder_time',
        'max_reminders', 'resume', 'resume_template',
        'sent_count', 'failure_count', 'created_at', 'reminder_count', 'deactivate'
    )

    def display_subject(self, obj):
        return obj.subject_template.subject if obj.subject_template else obj.subject
    display_subject.short_description = 'Subject'
    display_subject.admin_order_field = 'subject'


# ColdEmailLog Admin
@admin.register(ColdEmailLog)
class ColdEmailLogAdmin(admin.ModelAdmin):
    list_display = ('email_reminder', 'sent_date', 'sent_time')
    search_fields = ('email_reminder__subject', 'sent_date')
    list_filter = ('sent_date',)


# PersonalEmailReminder Admin
@admin.register(PersonalEmailReminder)
class PersonalEmailReminderAdmin(MarkdownxModelAdmin):
    list_display = (
        'display_subject', 'recipient', 'scheduled_time', 'scheduled_day_of_week',
        'scheduled_time_of_day', 'sent_count', 'failure_count', 'created_at'
    )
    search_fields = ('subject', 'recipient')
    list_filter = ('scheduled_day_of_week', 'created_at')
    readonly_fields = ('sent_count', 'failure_count', 'created_at')
    fields = (
        'recipient', 'notification_method',
        'subject', 'subject_template', 'body',
        'scheduled_time', 'scheduled_day_of_week', 'scheduled_time_of_day',
        'sent_count', 'failure_count', 'created_at', 'deactivate'
    )

    def display_subject(self, obj):
        return obj.subject_template.subject if obj.subject_template else obj.subject
    display_subject.short_description = 'Subject'
    display_subject.admin_order_field = 'subject'


# PersonalEmailLog Admin
@admin.register(PersonalEmailLog)
class PersonalEmailLogAdmin(admin.ModelAdmin):
    list_display = ('email_reminder', 'sent_date', 'sent_time')
    search_fields = ('email_reminder__subject', 'sent_date')
    list_filter = ('sent_date',)


# MessageTemplate Admin
@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'message_type', 'is_default', 'updated_at')
    search_fields = ('title',)
    list_filter = ('message_type', 'is_default')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('title', 'message_type', 'message', 'is_default', 'created_at', 'updated_at')


# SubjectTemplate Admin
@admin.register(SubjectTemplate)
class SubjectTemplateAdmin(admin.ModelAdmin):
    list_display = ('subject', 'is_default', 'updated_at')
    search_fields = ('subject',)
    list_filter = ('is_default',)
    readonly_fields = ('created_at', 'updated_at')
    fields = ('subject', 'is_default', 'created_at', 'updated_at')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_default', 'updated_at')
    search_fields = ('title',)
    list_filter = ('is_default',)
    readonly_fields = ('created_at', 'updated_at')
    fields = ('title', 'file', 'is_default', 'created_at', 'updated_at')
