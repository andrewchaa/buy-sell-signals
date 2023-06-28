# import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import pandas_ta as ta
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go

CLOSE = "Close"

df = yf.Ticker('^IXIC').history(period='1y')
df.ta.macd(close=CLOSE, fast=12, slow=26, signal=9, append=True)
# pd.set_option('display.max_columns', None)
df.columns = [x.lower() for x in df.columns]

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
        y=df['macd_12_26_9'],
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
        y=df['macds_12_26_9'],
        line=dict(color='#000000', width=2),
        # showlegend=False,
        legendgroup='2',
        name='signal'
    ), row=2, col=1
)
# Colorize the histogram values
colors = np.where(df['macdh_12_26_9'] < 0, '#000', '#ff9900')
# Plot the histogram
fig.append_trace(
    go.Bar(
        x=df.index,
        y=df['macdh_12_26_9'],
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

def get_cross_ema(df, short_period=9, long_period=26):
    ema_short = df[CLOSE].ewm(span=short_period, adjust=False).mean()
    ema_long = df[CLOSE].ewm(span=long_period, adjust=False).mean()

    signals = pd.DataFrame(index=df.index)
    signals[CLOSE] = df[CLOSE]
    signals['ema_short'] = ema_short
    signals['ema_long'] = ema_long
    signals['ema_cross'] = ema_short - ema_long
    signals['ema_positions'] = 0.0
    signals['ema_signal'] = np.where(signals['ema_cross'] > 0, 1.0, -1.0)
    signals['ema_positions'] = signals['ema_signal'].diff()

    return signals

def get_ema(df, period=9):
    signals = pd.DataFrame(index=df.index)
    signals[CLOSE] = df[CLOSE]
    signals['ema'] = df[CLOSE].ewm(span=period, adjust=False).mean()
    signals['ema_positions'] = 0.0
    signals['ema_signal'] = np.where(signals['ema'] < df[CLOSE], 1.0, 0)
    signals['ema_positions'] = signals['ema_signal'].diff()

    return signals


def get_ema_basic(df):
    alpha = 0.1
    signals = pd.DataFrame(index=df.index)

    signals['ema_signal'] = 0.0
    signals['ema'] = df[CLOSE].ewm(alpha=alpha, adjust=False).mean()
    signals[CLOSE] = df[CLOSE]
    signals['ema_positions'] = 0.0

    signals['ema_signal'] = np.where(signals['ema'] < df[CLOSE], 1.0, 0.0)
    signals['ema_positions'] = signals['ema_signal'].diff()
    return signals


def get_figure_ema(df, signals, name):
    fig = plt.figure(figsize=(12, 10))
    ax1 = fig.add_subplot(111, ylabel='Price in $')

    df.loc['2018-01-01':, CLOSE].plot(ax=ax1,
                                      color='r', lw=2., label=f'{name} Close Price')
    signals.loc[:, 'ema'].plot(ax=ax1, lw=2., label=f'{name} EMA')

    # Plot the buy signals
    ax1.plot(signals.loc[signals.ema_positions == 1.0].index,
             signals.ema[signals.ema_positions == 1.0],
             '^', markersize=10, color='g')

    # Plot the sell signals
    ax1.plot(signals.loc[signals.ema_positions == -1.0].index,
             signals.ema[signals.ema_positions == -1.0],
             'v', markersize=10, color='r')

    plt.legend()
    return fig


def get_figure(df, signals, name):
    fig = plt.figure(figsize=(12, 10))
    ax1 = fig.add_subplot(111, ylabel='Price in $')

    df.loc[:, CLOSE].plot(ax=ax1, color='r', lw=2., label=f'{name} Close Price')
    signals.loc[:, 'ema_short'].plot(
        ax=ax1, lw=2., label=f'{name} 9-period EMA')
    signals.loc[:, 'ema_long'].plot(
        ax=ax1, lw=2., label=f'{name} 26-period EMA')

    # Plot the buy signals
    buy_signals = signals.loc[signals.ema_positions == 2.0]
    ax1.plot(buy_signals.index,
             buy_signals['ema_short'], '^', markersize=10, color='g', label='Buy')

    # Plot the sell signals
    sell_signals = signals.loc[signals.ema_positions == -2.0]
    ax1.plot(sell_signals.index,
             sell_signals['ema_short'], 'v', markersize=10, color='r', label='Sell')

    plt.legend()
    return fig

def get_ema_figure(df, signals, period, name):
    fig = plt.figure(figsize=(12, 10))
    ax1 = fig.add_subplot(111, ylabel='Price in $')

    df.loc[:, CLOSE].plot(ax=ax1, color='r', lw=2., label=f'{name} Close Price')
    signals.loc[:, 'ema'].plot(ax=ax1, lw=2., label=f'{name} {period} period EMA')

    # Plot the buy signals
    buy_signals = signals.loc[signals.ema_positions == 1.0]
    ax1.plot(buy_signals.index,
             buy_signals['ema'], '^', markersize=10, color='g', label='Buy')

    # Plot the sell signals
    sell_signals = signals.loc[signals.ema_positions == -1.0]
    ax1.plot(sell_signals.index,
             sell_signals['ema'], 'v', markersize=10, color='r', label='Sell')

    plt.legend()
    return fig
