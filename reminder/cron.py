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
        print("cold email", len(cold_reminders))

        for reminder in cold_reminders:
            should_send, mail_type = reminder.should_send_email()
            if should_send:
                try:
                    original_message_id = None
                    last_log = ColdEmailLog.objects.filter(email_reminder=reminder).order_by('-sent_date').first()
                    if last_log:
                        original_message_id = last_log.message_id

                    # Get subject
                    subject = reminder.subject or (
                        reminder.subject_template.subject if reminder.subject_template else ""
                    )

                    # Get body content based on type
                    if mail_type == 'reminder':
                        body_html = (
                                reminder.reminder_template or
                                (
                                    reminder.reminder_message_template.message if reminder.reminder_message_template else "")
                        )
                    else:  # main_email
                        body_html = (
                                reminder.body or
                                (reminder.main_message_template.message if reminder.main_message_template else "")
                        )

                    new_message_id = send_reminder_email(
                        reminder.recipients,
                        subject,
                        body_html=body_html,
                        original_message_id=original_message_id
                    )
                    reminder.log_email_sent(is_reminder=(mail_type == 'reminder'), message_id=new_message_id)

                except Exception as e:
                    # Log the failure and handle failure count
                    reminder.log_email_failed(is_reminder=(mail_type == 'reminder'))

                    # If failed more than 3 times, send an alert
                    if (mail_type == 'reminder' and reminder.reminder_failure_count >= 3) or \
                            (mail_type == 'main_email' and reminder.failure_count >= 3):
                        self.send_alert(reminder)

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
                    print(f"Notification failed for reminder {reminder.id}: {e}")
                    reminder.log_notification_failed()

                    if reminder.failure_count >= 3:
                        self.send_alert(reminder)

    def send_alert(self, reminder):
        """Send an alert email when an email fails 3 times."""
        alert_subject = f"Email failed 3 times for {reminder.subject}"
        alert_message = f"Email to {reminder.recipients if hasattr(reminder, 'recipients') else reminder.recipient} failed 3 times. Please investigate."
        send_reminder_email(settings.EMAIL_HOST_USER, alert_subject, f"<p>{alert_message}</p>", alert_message)



