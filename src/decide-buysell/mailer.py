import base64
import os
import sendgrid
from sendgrid.helpers.mail import *


def send(to_emails, subject, html_content, charts):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    message = Mail()
    message.from_email = From(os.environ.get('SENDGRID_FROM_EMAIL'))
    message.to = [To(email=to_emails)]
    message.subject = Subject(subject)
    message.content = [
        Content(
            mime_type="text/html",
            content=html_content
        )
    ]

    attachments = []
    for chart in charts:
        with open(chart, 'rb') as f:
            img_data = f.read()
            img_data_b64 = base64.b64encode(img_data).decode()
            f.close()

        attachments.append(
            Attachment(
                FileContent(img_data_b64),
                FileName(chart),
                FileType('image/png'),
                Disposition('attachment')
            ))

    message.attachment = attachments

    sg.client.mail.send.post(request_body=message.get())
