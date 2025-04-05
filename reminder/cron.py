from django_cron import CronJobBase, Schedule

from .bot import send_telegram_message
from .mail import send_reminder_email
from .models import ColdEmailReminder, PersonalEmailReminder, ColdEmailLog
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
import markdown  # Ensure markdown is imported if you're using it for body_html conversion
from django.conf import settings
from django.utils.html import strip_tags

class SendEmailCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Adjust this based on your needs

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'reminder.send_email'

    def do(self):
        # Handle ColdEmailReminders
        cold_reminders = ColdEmailReminder.objects.filter(deactivate=False)

        for reminder in cold_reminders:
            should_send, mail_type = reminder.should_send_email()
            if should_send:
                try:
                    original_message_id = None
                    last_log = ColdEmailLog.objects.filter(email_reminder=reminder).order_by('-sent_date').first()
                    if last_log:
                        original_message_id = last_log.message_id

                    # Subject
                    subject = reminder.subject or (
                        reminder.subject_template.subject if reminder.subject_template else ""
                    )

                    # Body
                    if mail_type == 'reminder':
                        body_html = (
                                reminder.reminder_template or
                                (
                                    reminder.reminder_message_template.message if reminder.reminder_message_template else "")
                        )
                        resume_file_path = None  # No resume on reminders
                    else:
                        body_html = (
                                reminder.body or
                                (reminder.main_message_template.message if reminder.main_message_template else "")
                        )
                        # Resume for first email
                        resume_file_path = reminder.resume.path if reminder.resume else (
                            reminder.resume_template.file.path if reminder.resume_template else None
                        )

                    new_message_id = send_reminder_email(
                        reminder.recipients,
                        subject=subject,
                        body_html=body_html,
                        original_message_id=original_message_id,
                        resume_attachment_path=resume_file_path  # You must support this in your mail function
                    )

                    reminder.log_email_sent(is_reminder=(mail_type == 'reminder'), message_id=new_message_id)

                except Exception as e:
                    print(e)
                    reminder.log_email_failed(is_reminder=(mail_type == 'reminder'))
                    if (mail_type == 'reminder' and reminder.reminder_failure_count == 5) or \
                            (mail_type == 'main_email' and reminder.failure_count == 5):
                        self.send_alert(reminder.recipients, e)

        # Handle PersonalEmailReminders
        personal_reminders = PersonalEmailReminder.objects.filter(deactivate=False)

        for reminder in personal_reminders:

            if reminder.should_send_notification():  # updated method name
                try:
                    # Track if at least one notification succeeded
                    success = False

                    # Send email if needed
                    if reminder.notification_method in ['email', 'both']:
                        send_reminder_email(reminder.recipient, reminder.subject, reminder.body)
                        success = True

                    # Send Telegram message if needed
                    if reminder.notification_method in ['telegram', 'both']:
                        subject = reminder.subject if reminder.subject else reminder.subject_template.subject
                        send_telegram_message(
                            message=subject + ": " + strip_tags(reminder.body)
                        )
                        success = True

                    if success:
                        reminder.log_notification_sent()
                    else:
                        raise Exception("No notification method succeeded.")

                except Exception as e:
                    print(e)
                    print(f"Notification failed for reminder {reminder.id}: {e}")
                    reminder.log_notification_failed()

                    if reminder.failure_count == 5:
                        self.send_alert(reminder.recipient, e)

    def send_alert(self, subject, message):
        """Send an alert email when an email fails 3 times."""
        alert_subject = f"ALERT: Email failed 5 times"
        send_reminder_email(settings.EMAIL_HOST_USER, alert_subject, message)



