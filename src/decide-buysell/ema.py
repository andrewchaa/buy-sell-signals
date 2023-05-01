import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

CLOSE = "Close"


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
