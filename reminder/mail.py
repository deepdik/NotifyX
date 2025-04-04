import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
import markdown
from django.conf import settings


def send_reminder_email(receiver_email, subject, body_html=None, body_plain=None, original_message_id=None):

    # Your Gmail credentials
    sender_email = settings.EMAIL_HOST_USER
    sender_password = settings.EMAIL_HOST_PASSWORD
    sender_name = settings.SENDER_NAME

    if not original_message_id:
        # Create the initial email message
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
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = receiver_email

        # Generate and store the Message-ID for threading
        original_message_id = make_msgid(domain="gmail.com")
        msg['Message-ID'] = original_message_id

        # Setup the secure SSL context and send the initial email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("######## Original Email Sent Successfully #######")

    else:
        # Now, to send a reminder email in the same thread
        reminder_msg = EmailMessage()
        # Check if body_plain is given; if not, only HTML email will be sent
        if body_plain:
            # If a plain text version is provided, set it as the main content
            reminder_msg.set_content(body_plain)
        else:
            # If no plain text is provided, ensure body_html exists and convert to HTML
            if body_html:
                body_html = markdown.markdown(body_html)  # Convert Markdown to HTML
                # Add the HTML version of the email
                reminder_msg.add_alternative(body_html, subtype='html')

        reminder_msg['Subject'] = "RE: " + subject  # Prefix with "Re:" to indicate a response
        print(subject)
        reminder_msg['From'] = formataddr((sender_name, sender_email))
        reminder_msg['To'] = receiver_email

        # Set In-Reply-To and References headers to link to the original email thread
        reminder_msg['In-Reply-To'] = original_message_id
        reminder_msg['References'] = original_message_id
        # Setup the secure SSL context and send the reminder email
        context = ssl.create_default_context()
        # Send the reminder email in the same thread
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, reminder_msg.as_string())
            print("######## Reminder Email Sent Successfully in Same Thread #######")

    return original_message_id  # Return Message-ID for storage


def send_email(receiver_email, subject, body_html=None, body_plain=None):

    # Your Gmail credentials
    sender_email = settings.EMAIL_HOST_USER
    sender_password = settings.EMAIL_HOST_PASSWORD  # Use an App Password if you have 2FA enabled
    sender_name = settings.SENDER_NAME  # Desired display name

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
    msg['From'] = formataddr((sender_name, sender_email))  # Use formataddr to set the display name
    msg['To'] = receiver_email

    # Setup the secure SSL context
    context = ssl.create_default_context()

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("######## Email Sent Successfully #######")
