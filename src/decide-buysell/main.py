import yfinance as yf
from sendgrid.helpers.mail import *
import ema
import mailer

tickers = ["^IXIC", "GC=F", "^N225"]
names = ["Nasdaq", "Gold", "Nikkei 225"]
charts = []
content = ''
html_content = ''

for i, ticker in enumerate(tickers):
    data = yf.Ticker(ticker)
    df = ema.get_data(data)
    signals = ema.get_signals(df)
    chart = ema.get_figure(df, signals)
    chart_file = f'Signals-{names[i]}.png'
    chart.savefig(chart_file)
    charts.append(chart_file)

    content += f'EMA Signals for {names[i]}: \n'
    content += f'{signals.tail()}\n\n'
    print(content)

    html_content += f'<p>EMA Signals for {names[i]}:</p>\n'
    html_content += f'{signals.tail().to_html()}<br /><br />\n\n'

mailer.send(html_content, charts)
