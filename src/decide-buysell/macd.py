# https://www.alpharithms.com/calculate-macd-python-272222/
# import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import pandas_ta as ta
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd
import pandas_ta as ta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


df = yf.Ticker('AAPL').history(period='1y', interval='1d')
# df.set_index(pd.DatetimeIndex(df['Date']), inplace=True)
df.ta.macd(close="Close", fast=12, slow=26, signal=9, append=True)

# Calculate the MACD and Signal line difference
df['macd_signal_diff'] = df['macd'] - df['macds']

# Identify the points where the MACD line crosses the Signal line
df['macd_cross'] = df['macd_signal_diff'].apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)

# Identify the points where the MACD line crosses above the Signal line
# df['macd_cross_above'] = ((df['macd_cross'] > df['macd_cross'].shift(1)) & (df['macd_cross'] == 1))

# Identify the points where the MACD line crosses below the Signal line
# df['macd_cross_below'] = ((df['macd_cross'] < df['macd_cross'].shift(1)) & (df['macd_cross'] == -1))

print(df)

df.columns = [x.lower() for x in df.columns]
# Construct a 2 x 1 Plotly figure
fig = make_subplots(rows=2, cols=1)
# price Line
fig.append_trace(
    go.Scatter(
        x=df.index,
        y=df['open'],
        line=dict(color='#ff9900', width=1),
        name='open',
        # showlegend=False,
        legendgroup='1',
    ), row=1, col=1
)
# Candlestick chart for pricing
fig.append_trace(
    go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='#ff9900',
        decreasing_line_color='black',
        showlegend=False
    ), row=1, col=1
)
# Fast Signal (%k)
fig.append_trace(
    go.Scatter(
        x=df.index,
        y=df['macd'],
        line=dict(color='#ff9900', width=2),
        name='macd',
        # showlegend=False,
        legendgroup='2',
    ), row=2, col=1
)
# Slow signal (%d)
fig.append_trace(
    go.Scatter(
        x=df.index,
        y=df['macds'],
        line=dict(color='#000000', width=2),
        # showlegend=False,
        legendgroup='2',
        name='signal'
    ), row=2, col=1
)
# Colorize the histogram values
colors = np.where(df['macdh'] < 0, '#000', '#ff9900')
# Plot the histogram
fig.append_trace(
    go.Bar(
        x=df.index,
        y=df['macdh'],
        name='histogram',
        marker_color=colors,
    ), row=2, col=1
)
# Make it pretty
layout = go.Layout(
    plot_bgcolor='#efefef',
    # Font Families
    font_family='Monospace',
    font_color='#000000',
    font_size=20,
    xaxis=dict(
        rangeslider=dict(
            visible=False
        )
    )
)
# Update options and show plot
fig.update_layout(layout)
fig.show()
