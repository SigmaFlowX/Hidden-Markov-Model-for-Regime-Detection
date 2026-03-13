import pandas as pd
import os
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def add_log_returns(df, horizons):
    for n in horizons:
        df[f'log_returns_{n}'] = np.log(df['close'] / df['close'].shift(n))
    return df

def add_volatility(df, windows):
    log_returns = np.log(df['close']).diff()

    for w in windows:
        df[f'volatility_{w}'] = log_returns.rolling(w).std()

    return df

def main():
    pass

if __name__ == "__main__":
    main()