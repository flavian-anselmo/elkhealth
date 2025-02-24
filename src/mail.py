import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class SendMail:
    @staticmethod
    def send_email(subject, body, to_email, attachment_path=None):
        from_email = ""
        from_password = ""
        
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        if attachment_path:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment_path)}'
                )
                message.attach(part)
        
        try:
            server = smtplib.SMTP("smtp.office365.com", 587)
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, message.as_string())
            server.close()
            logger.info("Email sent successfully!")
        except Exception as e:
            logger.error(f"Error sending email: {e}")
        