from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import *

def sendEmailToSingleUser(body, to, subject):
    """Method to send Email to single User"""

    sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)
    from_email = Email(settings.DEFAULT_FROM_EMAIL)
    to_email = To(to)
    content = Content("text/html", body)
    mail = Mail(from_email, to_email, subject, content)
    try:
        sg.client.mail.send.post(request_body=mail.get())
    except Exception as e:
        print(e)
        pass
    
    return