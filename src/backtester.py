import pandas as pd
import numpy as np


def backtest(df, z_entry, z_exit, z_window):
    mean = df['close'].rolling(window=z_window).mean()
    std = df['close'].rolling(window=z_window).std()

    df['z_score'] = (df['close'] - mean)/std
    df.dropna(inplace=True)


def main():
    df = pd.read_csv("../data/SBER.csv")
    df['timestamp'] = pd.to_datetime(df['begin'])
    df.set_index('timestamp', inplace=True)
    df = df[['close']]

    backtest(df, 2, 0.5, 20)

if __name__ == "__main__":
    main()