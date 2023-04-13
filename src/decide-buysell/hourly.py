import os
import numpy as np
import yfinance as yf
from sendgrid.helpers.mail import *
from datetime import date
import ema
import mailer

tickers = ["^IXIC", "GC=F", "^N225"]
names = ["Nasdaq", "Gold", "Nikkei 225"]
charts = []

for i, ticker in enumerate(tickers):
    content = ''
    html_content = ''
    yfTicker = yf.Ticker(ticker)
    dailyDf = yfTicker.history(period="3mo", interval="1d")
    signals = ema.get_signals(dailyDf)
    latest_ema = signals.tail(1)['ema'].values[0]

    hourlyDf = yfTicker.history(period="1d", interval="1h")
    reviewDf = hourlyDf[['Close']].tail(3)
    reviewDf['Ema'] = latest_ema
    reviewDf['Signal'] = np.where(
        reviewDf['Close'] > reviewDf['Ema'], 1.0, 0.0)
    reviewDf['Signal_Position'] = reviewDf['Signal'].diff()

    content += f'Hourly data for {names[i]}: \n'
    content += f'{reviewDf}\n\n'
    print(content)

    html_content += f'<p>Hourly alert for {names[i]}:</p>\n'
    html_content += f'{reviewDf.to_html()}<br /><br />\n\n'
    if (reviewDf['Signal_Position'] == 1.0).any():
        to_emails = os.environ.get('SENDGRID_TO_EMAILS').split(',')
        mailer.send(
            to_emails, f"Hourly Signal alerts on {date.today()} for {names[i]} ", html_content, [])