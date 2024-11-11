from django.core.exceptions import ValidationError
from django.utils import timezone
from markdownx.models import MarkdownxField
from django.db import models

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


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
        help_text="Enter the subject of the email."
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

    def clean(self):
        # Validate that reminder_template or plain_reminder_template is required if reminder_frequency is not
        # "no_reminder"
        if self.reminder_frequency != 'no_reminder' and not self.reminder_template:
            raise ValidationError(
                "You must a markdown reminder template when setting a "
                "reminder.")

    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject

    def should_send_email(self):
        """Determine if the email should be sent based on schedule or instant send options."""
        now = timezone.localtime(timezone.now())  # Use local time
        # Instant send logic
        if self.instant_send and not self.email_already_sent():
            return True, 'main_email'

        # Scheduled send logic
        if self.scheduled_time and now >= self.scheduled_time and not self.email_already_sent():
            return True, 'main_email'

        # Reminder send logic
        if self.reminder_frequency != 'no_reminder' and self.reminder_count < self.max_reminders:
            if self.reminder_should_be_sent(now):
                return True, 'reminder'

        return False, None  # If no email needs to be sent

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

    def log_email_sent(self, is_reminder=False):
        """Log the email as sent by creating a ColdEmailLog entry."""
        now = timezone.localtime(timezone.now())
        ColdEmailLog.objects.create(email_reminder=self, sent_date=now.date(), is_reminder=is_reminder)

        if is_reminder:
            self.reminder_count += 1
            self.reminder_failure_count = 0  # Reset failure count for reminders
        else:
            self.sent_count += 1
            self.failure_count = 0  # Reset failure count for main email
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
    sent_date = models.DateField()  # Track the date when the email was sent
    sent_time = models.TimeField(auto_now_add=True)  # Track the time when the email was sent
    is_reminder = models.BooleanField(default=False)  # Track whether this was a reminder


    def __str__(self):
        return f"Email for {self.email_reminder.subject} sent on {self.sent_date} at {self.sent_time}"


class PersonalEmailReminder(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = RichTextUploadingField()

    scheduled_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="For one-time Email only. Choose this if the email is to be sent at a specific date and time."
    )

    # Recurring email based on the day of the week
    scheduled_day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
            ('All days', 'All days')
        ],
        null=True,
        blank=True,
        help_text="For recurring emails. Select the day(s) of the week on which to send the email."
    )

    # Time of day for recurring emails
    scheduled_time_of_day = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of day to send the email if a recurring day is selected."
    )

    created_at = models.DateTimeField(default=timezone.now)
    sent_count = models.IntegerField(default=0)  # Track how many times the email has been sent
    failure_count = models.IntegerField(default=0)  # Track consecutive failures
    deactivate = models.BooleanField(default=False)

    def clean(self):
        # Ensure that either `scheduled_time` or `scheduled_day_of_week` is selected, but not both
        if self.scheduled_time and self.scheduled_day_of_week:
            raise ValidationError("You cannot select both 'Scheduled Time' and 'Scheduled Day of Week'. Choose one.")

        if not self.scheduled_time and not self.scheduled_day_of_week:
            raise ValidationError("You must select either 'Scheduled Time' for a one-time email or 'Scheduled Day of Week' for recurring emails.")

        # If `scheduled_day_of_week` is selected, `scheduled_time_of_day` must be selected
        if self.scheduled_day_of_week and not self.scheduled_time_of_day:
            raise ValidationError("When selecting 'Scheduled Day of Week', you must also select 'Scheduled Time of Day'.")

        super().clean()

    def __str__(self):
        return f"Email Schedule: {self.scheduled_time or self.scheduled_day_of_week}"


    def should_send_email(self):
        """Determine if the email should be sent based on schedule or day of the week."""
        # Get the current time in UTC
        now_utc = timezone.now()
        # Convert it to the local time zone (America/Chicago)
        now = timezone.localtime(now_utc)
        # If scheduled for a specific date and it hasn't been sent, send it
        print(now)
        # print(now >= self.scheduled_time )
        print(self.sent_count)
        print(self.email_already_sent())
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

    def log_email_sent(self):
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
