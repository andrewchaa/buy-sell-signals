import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import ema

df = ema.get_nasdaq_data()
signals = ema.get_signals(df)
chart = ema.get_figure(df, signals)


def handler():
    chart.savefig('signals.png')
    print(signals.tail())
