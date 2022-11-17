import logging

from django.core.mail import EmailMessage


class SendEmail:
    @staticmethod
    def send_email(subject, body, to, **kwargs):
        try:
            email = EmailMessage(subject=subject, body=body, to=to, **kwargs)
            return email.send()

        except Exception as e:
            logging.error(f"There was an error sending an email. \n{e}")
