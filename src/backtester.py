import pandas as pd
import numpy as np


def backtest(df, z_entry, z_exit, z_window):
    mean = df['close'].rolling(window=z_window).mean()
    std = df['close'].rolling(window=z_window).std()

    df['z_score'] = (df['close'] - mean)/std
    df.dropna(inplace=True)

    position = 0
    positions = []
    for z in df['z_score']:
        if position == 0:
            if z < -z_entry:
                position = 1
            elif z > z_entry:
                position = -1
        elif position == 1:
            if z >= -z_exit:
                position = 0
        elif position == -1:
            if z <= z_exit:
                position = 0
        positions.append(position)

    df['position'] = positions

    print(df.head())

def main():
    df = pd.read_csv("../data/SBER.csv")
    df['timestamp'] = pd.to_datetime(df['begin'])
    df.set_index('timestamp', inplace=True)
    df = df[['close']]

    backtest(df, 1, 0.5, 20)

if __name__ == "__main__":
    main()