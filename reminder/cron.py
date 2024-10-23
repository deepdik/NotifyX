import smtplib
import ssl
from email.message import EmailMessage

from django_cron import CronJobBase, Schedule
from .models import ColdEmailReminder, PersonalEmailReminder
import markdown  # To convert markdown to HTML


def send_reminder_email(receiver_email, subject, body_html=None, body_plain=None):
    # Your Gmail credentials
    sender_email = "dk5f1995@gmail.com"
    sender_password = "dexh vzvb geoz fqgc"  # Use an App Password if you have 2FA enabled

    # Create the email message
    msg = EmailMessage()

    # Check if body_plain is given; if not, only HTML email will be sent
    if body_plain:
        # If a plain text version is provided, set it as the main content
        msg.set_content(body_plain)
    else:
        # If no plain text is provided, ensure body_html exists and convert to HTML
        if body_html:
            body_html = markdown.markdown(body_html)  # Convert Markdown to HTML
            # Add the HTML version of the email
            msg.add_alternative(body_html, subtype='html')

    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Setup the secure SSL context
    context = ssl.create_default_context()

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)  # Uncomment for actual use
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Uncomment for actual use
        print("######## Email Sent Successfully #######")


class SendEmailCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Adjust this based on your needs

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'reminder.send_email'

    def do(self):
        # Handle ColdEmailReminders
        cold_reminders = ColdEmailReminder.objects.filter(deactivate=False)
        for reminder in cold_reminders:
            should_send, mail_type = reminder.should_send_email()  # Get whether to send and mail type

            if should_send:
                try:
                    # Use the appropriate email body for reminders or main emails
                    if mail_type == 'reminder':
                        send_reminder_email(
                            reminder.recipients,
                            reminder.subject,
                            body_html=reminder.reminder_template
                        )
                    else:
                        send_reminder_email(reminder.recipients, reminder.subject, body_html=reminder.body)

                    # Log the email send as either a main email or a reminder
                    reminder.log_email_sent(is_reminder=(mail_type == 'reminder'))  # Log success

                except Exception as e:
                    # Log the failure and handle failure count
                    reminder.log_email_failed(is_reminder=(mail_type == 'reminder'))  # Log failure

                    # If failed more than 3 times, send an alert
                    if (mail_type == 'reminder' and reminder.reminder_failure_count >= 3) or \
                            (mail_type == 'main_email' and reminder.failure_count >= 3):
                        self.send_alert(reminder)

        # Handle PersonalEmailReminders
        personal_reminders = PersonalEmailReminder.objects.filter(deactivate=False)
        for reminder in personal_reminders:
            if reminder.should_send_email():
                try:
                    send_reminder_email(reminder.recipient, reminder.subject, reminder.body)
                    reminder.log_email_sent()  # Log success
                except Exception as e:
                    reminder.log_email_failed()  # Log failure
                    if reminder.failure_count >= 3:
                        self.send_alert(reminder)

    def send_alert(self, reminder):
        """Send an alert email when an email fails 3 times."""
        alert_subject = f"Email failed 3 times for {reminder.subject}"
        alert_message = f"Email to {reminder.recipients if hasattr(reminder, 'recipients') else reminder.recipient} failed 3 times. Please investigate."
        send_reminder_email('deep.kumar2052@gmail.com', alert_subject, f"<p>{alert_message}</p>", alert_message)
