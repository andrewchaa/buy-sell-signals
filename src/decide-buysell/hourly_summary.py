from datetime import date
import os
import yfinance as yf
from sendgrid.helpers.mail import *
import ema
import mailer

DIR = 'charts'
tickers = ["^IXIC", "GC=F", "^N225", "^FTSE", "^GDAXI"]
names = ["Nasdaq", "Gold", "Nikkei 225", "UK 100", "Germany 40"]
charts = []
content = ''
html_content = ''

for i, ticker in enumerate(tickers):
    df = yf.Ticker(ticker).history(period="5d", interval="1h")
    signals = ema.get_cross_ema(df, short_period=9, long_period=26)
    if not os.path.exists(DIR):
        os.makedirs(DIR)

    chart = ema.get_figure(df, signals, names[i])
    chart_file = f'{DIR}/Signals-{names[i]}.png'
    chart.savefig(chart_file)
    charts.append(chart_file)

    content += f'EMA Signals for {names[i]}: \n'
    content += f'{signals.tail()}\n\n'
    print(content)

    html_content += f'<p>EMA Signals for {names[i]}:</p>\n'
    html_content += f'{signals.tail().to_html()}<br /><br />\n\n'

to_emails = os.environ.get('SENDGRID_TO_EMAILS').split(',')
mailer.send(to_emails, f"EMA Signals for {date.today()}", html_content, charts)
