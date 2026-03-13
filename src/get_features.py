import pandas as pd
import os
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def compute_log_returns(df):
    returns = df['close'] / df['close'].shift(1).dropna()
    log_returns = np.log(returns)

    return log_returns

def main():
    pass

if __name__ == "__main__":
    main()