import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .enums import EmailFormat
from .schema import EmailMessage


def send_email(email_message: EmailMessage):
    """Send email message using SMTP."""
    # The mail addresses and password
    # Setup the MIME
    message = MIMEMultipart()
    message["From"] = email_message.sender_config.email
    message["To"] = ", ".join(email_message.recipients)
    message["Subject"] = email_message.subject
    # The subject line
    # The body and the attachments for the mail
    if email_message.format == EmailFormat.HTML:
        message.add_header("Content-Type", "text/html")
    message.attach(MIMEText(email_message.content, email_message.format.value))
    if email_message.attachments is not None:
        for attachment in email_message.attachments:
            attach_file = open(attachment, "rb")  # Open the file as binary mode
            payload = MIMEBase("application", "octate-stream")
            payload.set_payload(attach_file.read())
            encoders.encode_base64(payload)  # encode the attachment
            # add payload header with filename
            fn = os.path.basename(attachment)
            payload.add_header(
                "Content-Disposition",
                f"attachment; filename= {fn}",
            )
            message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(
        email_message.sender_config.email, email_message.sender_config.password
    )  # login with mail_id and password
    text = message.as_string()
    senders_response = session.sendmail(email_message.sender_config.email, email_message.recipients, text)
    session.quit()
    return senders_response
