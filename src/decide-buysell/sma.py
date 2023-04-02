import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def get_nasdaq_data():
    nasdaq = yf.Ticker("^IXIC")
    nasdaq_data = nasdaq.history(period="3mo", interval="1d")
    nasdaq_data.to_csv("nasdaq.csv")
    return nasdaq_data


def calculate_sma(data, period):
    sma = data["Close"].rolling(window=period).mean()
    return sma


def generate_signals(data):
    data["5_SMA"] = calculate_sma(data, 5)
    data["10_SMA"] = calculate_sma(data, 10)

    data["Signal"] = None
    for i in range(len(data)):
        if data["5_SMA"][i] > data["10_SMA"][i]:
            data["Signal"][i] = 'Buy'
        else:
            data["Signal"][i] = 'Sell'

    return data


def plot_graph(data):
    buy_signals = data[data['Signal'] == 'Buy']
    sell_signals = data[data['Signal'] == 'Sell']

    plt.figure(figsize=(15, 10))
    plt.plot(data.index, data["Close"], label="Nasdaq", alpha=0.5)
    plt.plot(data.index, data["5_SMA"],
             label="5 Day SMA", linestyle="--", alpha=0.7)
    plt.plot(data.index, data["10_SMA"],
             label="10 Day SMA", linestyle="--", alpha=0.7)
    plt.title("Nasdaq Buy/Sell Signals using 5 and 10 Day SMA")
    plt.scatter(buy_signals.index, data.loc[buy_signals.index]
                ['Close'], marker='^', color='g', label='Buy Signal')
    plt.scatter(sell_signals.index, data.loc[sell_signals.index]
                ['Close'], marker='v', color='r', label='Sell Signal')
    plt.xlabel("Date")
    plt.ylabel("Close Price ($)")
    plt.legend()
    plt.show()


def get_latest_signal(data):
    return data["Signal"][-1]


data = get_nasdaq_data()
data_with_signals = generate_signals(data)

latest_signal = get_latest_signal(data_with_signals)
print(f"Latest Signal: {latest_signal}")
plot_graph(data_with_signals)
