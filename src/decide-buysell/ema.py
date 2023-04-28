import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf


def get_signals_from_dataframe(df):
    alpha = 0.1
    signals = pd.DataFrame(index=df.index)

    signals['ema_signal'] = 0.0
    signals['ema'] = df['Close'].ewm(alpha=alpha, adjust=False).mean()
    signals['close'] = df['Close']
    signals['ema_positions'] = 0.0

    signals['ema_signal'] = np.where(signals['ema'] < df['Close'], 1.0, 0.0)
    signals['ema_positions'] = signals['ema_signal'].diff()
    return signals


def get_figure(df, signals, name):
    fig = plt.figure(figsize=(12, 10))
    ax1 = fig.add_subplot(111, ylabel='Price in $')

    df.loc['2018-01-01':, 'Close'].plot(ax=ax1,
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
