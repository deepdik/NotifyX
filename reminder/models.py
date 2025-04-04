from django.core.exceptions import ValidationError
from django.utils import timezone
from markdownx.models import MarkdownxField
from django.db import models

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from .gmail_api import check_reply_received


class SubjectTemplate(models.Model):
    subject = models.CharField(
        max_length=255,
        help_text="Reusable subject line for emails."
    )
    is_default = models.BooleanField(
        default=False,
        help_text="Mark this subject as default."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subject Template"
        verbose_name_plural = "Subject Templates"

    def __str__(self):
        return f"{self.subject}{' [Default]' if self.is_default else ''}"

    def clean(self):
        # Only one default allowed
        if self.is_default:
            SubjectTemplate.objects.exclude(pk=self.pk).update(is_default=False)

class ColdEmailReminder(models.Model):
    RECIPIENT_REMINDER_OPTIONS = [
        ('same_day', 'Same Day'),
        ('daily', 'Daily'),
        ('after_1_day', 'After 1 Day'),
        ('after_2_days', 'After 2 Days'),
        ('after_3_days', 'After 3 Days'),
        ('weekly', 'Weekly'),
        ('no_reminder', 'No Reminder'),
    ]

    recipients = models.CharField(
        max_length=255,
        help_text="Enter comma-separated email addresses to send the email to."
    )  # Comma-separated email list
    subject = models.CharField(
        max_length=255,
        help_text="Enter the subject of the email.",
        blank = True,
        null=True
    )
    body = RichTextUploadingField(
        blank=True,
        help_text="Enter the email body using Markdown. Leave blank if you're using plain text."
    )  # Markdown email body
    reminder_template = RichTextUploadingField(
        blank=True,
        help_text="Enter the Markdown reminder email template. Leave blank if you're using plain text for reminders."
    )  # Template used for the reminder
    instant_send = models.BooleanField(
        default=False,
        help_text="Check this box if you want to send the email immediately."
    )
    scheduled_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Set the date and time to schedule the email sending."
    )  # For scheduling email sending
    reminder_frequency = models.CharField(
        max_length=15,
        choices=RECIPIENT_REMINDER_OPTIONS,
        default='no_reminder',
        help_text="Select the frequency for sending reminders. Choose 'No Reminder' to disable reminders."
    )
    reminder_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Specify the time to send the reminder, if a reminder is set."
    )  # Specific time to send the reminder
    max_reminders = models.IntegerField(
        default=3,
        help_text="Specify the maximum number of reminders to send. Default is 3."
    )  # Max number of reminders, default is 3

    sent_count = models.IntegerField(default=0)  # Track how many times the main email has been sent
    reminder_count = models.IntegerField(default=0)  # Track how many times reminders have been sent
    created_at = models.DateTimeField(default=timezone.now)
    failure_count = models.IntegerField(default=0)  # Track consecutive failures for the main email
    reminder_failure_count = models.IntegerField(default=0)  # Track failures for reminder emails
    deactivate = models.BooleanField(default=False)

    main_message_template = models.ForeignKey(
        'MessageTemplate',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'message_type': 'main'},
        related_name='main_reminders',
        help_text="Select a reusable message template for the main email."
    )

    reminder_message_template = models.ForeignKey(
        'MessageTemplate',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'message_type': 'reminder'},
        related_name='reminder_reminders',
        help_text="Select a reusable message template for reminder emails."
    )

    subject_template = models.ForeignKey(
        'SubjectTemplate',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='email_reminders',
        help_text="Choose a predefined subject template."
    )

    def clean(self):
        errors = {}

        # Enforce either body or main message template is set
        if not self.body and not self.main_message_template:
            errors['body'] = "You must provide either a message body or select a main message template."

        # Enforce either subject or subject template is set
        if not self.subject and not self.subject_template:
            errors['subject'] = "You must provide either a subject or select a subject template."

        # Reminder content must be provided if reminder is enabled
        if self.reminder_frequency != 'no_reminder':
            if not self.reminder_template and not self.reminder_message_template:
                errors['reminder_template'] = (
                    "You must provide a reminder body or select a reminder message template if reminders are enabled."
                )

        if errors:
            raise ValidationError(errors)

        super().clean()

    def save(self, *args, **kwargs):
        if ',' in self.recipients:
            recipients = [email.strip() for email in self.recipients.split(',')]
            for email in recipients:
                ColdEmailReminder.objects.create(
                    recipients=email,
                    subject=self.subject,
                    body=self.body,
                    reminder_template=self.reminder_template,
                    instant_send=self.instant_send,
                    scheduled_time=self.scheduled_time,
                    reminder_frequency=self.reminder_frequency,
                    reminder_time=self.reminder_time,
                    max_reminders=self.max_reminders,
                )
            return  # Prevent saving original instance
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    # def should_send_email(self):
    #     """Determine if the email should be sent based on schedule or instant send options."""
    #     now = timezone.localtime(timezone.now())  # Use local time
    #     # Instant send logic
    #     if self.instant_send and not self.email_already_sent():
    #         return True, 'main_email'
    #
    #     # Scheduled send logic
    #     if self.scheduled_time and now >= self.scheduled_time and not self.email_already_sent():
    #         return True, 'main_email'
    #
    #     # Reminder send logic
    #     if self.reminder_frequency != 'no_reminder' and self.reminder_count < self.max_reminders:
    #         if self.reminder_should_be_sent(now):
    #             return True, 'reminder'
    #
    #     return False, None  # If no email needs to be sent

    def should_send_email(self):
        now = timezone.localtime(timezone.now())
        last_log = ColdEmailLog.objects.filter(email_reminder=self).order_by('-sent_date').first()

        # if last_log and last_log.message_id:
        #     if check_reply_received(last_log.message_id):
        #         print("Reply detected, skipping reminder.")
        #         return False, None

        if self.instant_send and not self.email_already_sent():
            return True, 'main_email'

        if self.scheduled_time and now >= self.scheduled_time and not self.email_already_sent():
            return True, 'main_email'

        # Reminder send logic
        if self.reminder_frequency != 'no_reminder' and self.reminder_count < self.max_reminders:
            if self.reminder_should_be_sent(now):
                return True, 'reminder'

        return False, None

    def reminder_should_be_sent(self, now):
        """Check if a reminder should be sent based on reminder_frequency and reminder_time."""
        if self.reminder_frequency == 'same_day':
            # Send reminder only once on the same day
            if now.time() >= self.reminder_time and not self.reminder_already_sent_today():
                return True

        elif self.reminder_frequency == 'daily' and self.sent_on_previous_day():
            return not self.reminder_already_sent_today()
        elif self.reminder_frequency == 'after_1_day' and self.sent_days_ago(1):
            return not self.reminder_already_sent_today()
        elif self.reminder_frequency == 'after_2_days' and self.sent_days_ago(2):
            return not self.reminder_already_sent_today()
        elif self.reminder_frequency == 'after_3_days' and self.sent_days_ago(3):
            return not self.reminder_already_sent_today()
        elif self.reminder_frequency == 'weekly' and self.sent_on_previous_week():
            return not self.reminder_already_sent_today()
        return False

    def email_already_sent(self):
        """Check if the main email has already been sent."""
        return ColdEmailLog.objects.filter(email_reminder=self, is_reminder=False).exists()

    def reminder_already_sent_today(self):
        """Check if a reminder has already been sent today."""
        now = timezone.localtime(timezone.now())  # Get the current local time
        today = now.date()  # Get the current date
        # Check the logs to see if a reminder was already sent today
        return ColdEmailLog.objects.filter(email_reminder=self, sent_date=today, is_reminder=True).exists()

    def sent_today(self):
        """Check if email was sent today."""
        now = timezone.localtime(timezone.now())
        today = now.date()
        return ColdEmailLog.objects.filter(email_reminder=self, sent_date=today).exists()

    def sent_on_date(self, date):
        """Check if email was sent on a specific date."""
        return ColdEmailLog.objects.filter(email_reminder=self, sent_date=date).exists()

    def sent_days_ago(self, days):
        """Check if the email was sent a certain number of days ago."""
        now = timezone.localtime(timezone.now())
        past_date = now.date() - timezone.timedelta(days=days)
        return self.sent_on_date(past_date)

    def sent_on_previous_day(self):
        """Check if the email was sent on the previous day."""
        return self.sent_days_ago(1)

    def sent_on_previous_week(self):
        """Check if the email was sent a week ago."""
        now = timezone.localtime(timezone.now())
        past_date = now.date() - timezone.timedelta(weeks=1)
        return self.sent_on_date(past_date)

    def log_email_sent(self, is_reminder=False, message_id=None):
        """Log the email as sent by creating a ColdEmailLog entry."""
        now = timezone.localtime(timezone.now())
        ColdEmailLog.objects.create(
            email_reminder=self,
            sent_date=now.date(),
            is_reminder=is_reminder,
            message_id=message_id
        )

        if is_reminder:
            self.reminder_count += 1
            self.reminder_failure_count = 0
        else:
            self.sent_count += 1
            self.failure_count = 0
        self.save()

    def log_email_failed(self, is_reminder=False):
        """Log a failed email send attempt and track failures."""
        if is_reminder:
            self.reminder_failure_count += 1
        else:
            self.failure_count += 1
        self.save()

        # If failed 3 times, notify admin
        if is_reminder and self.reminder_failure_count >= 3:
            self.notify_admin(failure_type='reminder')
        elif not is_reminder and self.failure_count >= 3:
            self.notify_admin(failure_type='main_email')

    def notify_admin(self, failure_type='main_email'):
        from NotifyX.reminder.cron import SendEmailCronJob
        """Send an email notification to the admin if the email failed 3 times."""
        subject = f"Email Failure Alert: {self.subject}"
        message = f"The {failure_type} has failed 3 times. Please check the logs."
        # You can use Django's send_mail or any email-sending logic
        SendEmailCronJob().send_alert()


class ColdEmailLog(models.Model):
    email_reminder = models.ForeignKey('ColdEmailReminder', on_delete=models.CASCADE)
    sent_date = models.DateField()
    sent_time = models.TimeField(auto_now_add=True)
    is_reminder = models.BooleanField(default=False)
    message_id = models.CharField(max_length=255, null=True, blank=True)  # Store Message-ID

    def __str__(self):
        return f"Email for {self.email_reminder.subject} sent on {self.sent_date} at {self.sent_time}"


class PersonalEmailReminder(models.Model):
    # Existing fields...
    recipient = models.EmailField(
        help_text="Used only if Email or Both is selected.",
        blank=True
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
        help_text="Used if a subject template is not selected."
    )
    subject_template = models.ForeignKey(
        SubjectTemplate,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='personal_reminders',
        help_text="Select a predefined subject template. Takes precedence over the custom subject field."
    )
    body = RichTextUploadingField()

    notification_method = models.CharField(
        max_length=10,
        choices=[
            ('email', 'Email Only'),
            ('telegram', 'Telegram Only'),
            ('both', 'Email and Telegram'),
        ],
        default='email',
        help_text="Choose how you want to be notified."
    )

    scheduled_time = models.DateTimeField(null=True, blank=True)
    scheduled_day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'), ('Friday', 'Friday'),
            ('Saturday', 'Saturday'), ('Sunday', 'Sunday'), ('All days', 'All days')
        ],
        null=True,
        blank=True
    )
    scheduled_time_of_day = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    sent_count = models.IntegerField(default=0)
    failure_count = models.IntegerField(default=0)
    deactivate = models.BooleanField(default=False)

    def clean(self):
        errors = {}

        if self.scheduled_time and self.scheduled_day_of_week:
            errors['scheduled_time'] = "You cannot select both 'Scheduled Time' and 'Scheduled Day of Week'."

        if not self.scheduled_time and not self.scheduled_day_of_week:
            errors['scheduled_time'] = "You must select either 'Scheduled Time' or 'Scheduled Day of Week'."

        if self.scheduled_day_of_week and not self.scheduled_time_of_day:
            errors['scheduled_time_of_day'] = "Time of day must be set for recurring reminders."

        if self.notification_method in ['email', 'both'] and not self.recipient:
            errors['recipient'] = "Recipient email is required for Email or Both notification method."

        if not self.subject and not self.subject_template:
            errors['subject'] = "Either a custom subject or a subject template must be selected."

        if errors:
            raise ValidationError(errors)

        super().clean()

    def get_subject(self):
        return self.subject_template.subject if self.subject_template else self.subject

    def __str__(self):
        return f"Reminder: {self.get_subject()} via {self.notification_method}"


    def should_send_notification(self):
        """Determine if the email should be sent based on schedule or day of the week."""
        # Get the current time in UTC
        now_utc = timezone.now()
        # Convert it to the local time zone (America/Chicago)
        now = timezone.localtime(now_utc)
        # If scheduled for a specific date and it hasn't been sent, send it
        if self.scheduled_time and now >= self.scheduled_time and self.sent_count == 0:
            print("outside ", self.email_already_sent())
            return not self.email_already_sent()

        # If scheduled for a specific day of the week and hasn't been sent, send it
        if self.scheduled_day_of_week:
            if self.scheduled_day_of_week == 'All days' or now.strftime('%A') == self.scheduled_day_of_week:
                print("inside ", self.scheduled_time_of_day)
                print("inside ", now.time())
                if self.scheduled_time_of_day and now.time() >= self.scheduled_time_of_day:
                    print("inside ", self.email_already_sent())
                    return not self.email_already_sent()

        return False

    def email_already_sent(self):
        """Check if the email has already been sent."""
        return PersonalEmailLog.objects.filter(email_reminder=self).exists()

    def log_notification_sent(self):
        """Log the email as sent."""
        now_utc = timezone.now()
        # Convert it to the local time zone (America/Chicago)
        now = timezone.localtime(now_utc)
        PersonalEmailLog.objects.create(email_reminder=self, sent_date=now.date())
        self.sent_count += 1
        self.failure_count = 0  # Reset failure count on successful send
        self.save()

    def log_email_failed(self):
        """Log a failed email send attempt."""
        self.failure_count += 1
        self.save()


class PersonalEmailLog(models.Model):
    email_reminder = models.ForeignKey('PersonalEmailReminder', on_delete=models.CASCADE)
    sent_date = models.DateField()  # Track the date when the email was sent
    sent_time = models.TimeField(auto_now_add=True)  # Track the time when the email was sent

    def __str__(self):
        return f"Personal email for {self.email_reminder.subject} sent on {self.sent_date} at {self.sent_time}"



class MessageTemplate(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('main', 'Main Email'),
        ('reminder', 'Reminder Email'),
    ]

    title = models.CharField(max_length=255)
    message = RichTextUploadingField()
    is_default = models.BooleanField(default=False)
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        help_text="Is this for the main email or a reminder?"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Message Template"
        verbose_name_plural = "Message Templates"

    def __str__(self):
        return f"{self.title} ({self.message_type}){' [Default]' if self.is_default else ''}"

    def clean(self):
        if self.is_default:
            MessageTemplate.objects.filter(
                message_type=self.message_type
            ).exclude(pk=self.pk).update(is_default=False)







