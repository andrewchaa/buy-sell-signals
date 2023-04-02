import base64
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import sendgrid
from sendgrid.helpers.mail import *
import ema

df = ema.get_nasdaq_data()
signals = ema.get_signals(df)
chart = ema.get_figure(df, signals)

chart.savefig('signals.png')
print(signals.tail())

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
message = Mail()

message.from_email = From(os.environ.get('SENDGRID_FROM_EMAIL'))
message.to = [
    To(email=os.environ.get(
        'SENDGRID_TO_EMAILS').split(','))]
message.subject = Subject("EMA Signals")
message.content = [
    Content(
        mime_type="text/html",
        content=signals.tail().to_html()
    )
]

image_filename = "signals.png"

with open(image_filename, 'rb') as f:
    img_data = f.read()
    img_data_b64 = base64.b64encode(img_data).decode()
    f.close()

message.attachment = [
    Attachment(
        FileContent(img_data_b64),
        FileName(image_filename),
        FileType('image/png'),
        Disposition('attachment')
    )]

response = sg.client.mail.send.post(request_body=message.get())
print(response.status_code)
