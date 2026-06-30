import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
import optuna
import matplotlib.pyplot as plt

def generate_walk_forward_windows(df, train_months=6, test_months=3):
    windows = []
    start_date = df.index.min()
    end_date = df.index.max()

    current_start = start_date

    while True:
        train_start = current_start
        train_end = train_start + relativedelta(months=train_months)
        test_start = train_end
        test_end = test_start + relativedelta(months=test_months)

        if test_end > end_date:
            break

        windows.append((train_start, train_end, test_start, test_end))
        current_start = train_start + relativedelta(months=test_months)

    return windows

def backtest(df, z_entry, z_exit, z_window):
    df = df.copy()

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

    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['position'].shift(1) * df['returns']
    df['equity'] = (1 + df['strategy_returns']).cumprod()

    return df

def objective(trial, df):
    df = df.copy()

    z_entry = trial.suggest_float('z_entry', 0.0, 5)
    z_exit = trial.suggest_float('z_exit', 0.0, z_entry)
    z_window = trial.suggest_int('z_window', 0, 100)

    df = backtest(df, z_entry, z_exit, z_window)

    daily_returns = (1 + df['strategy_returns']).resample('1D').prod() - 1
    sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252)

    return sharpe

def optimize(df, trials=200):
    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: objective(trial, df), n_trials=trials, n_jobs=-1)

    return study.best_params

def walk_forward_optimization(df, train_month, test_month, trials=200):
    df = df.copy()

    windows = generate_walk_forward_windows(df, train_month, test_month)

    results = []
    equity_point = 1.0
    for train_start, train_end, test_start, test_end in windows:
        train_df = df.loc[train_start:train_end].copy()
        test_df = df.loc[test_start:test_end].copy()

        params = optimize(train_df, trials)

        test_res = backtest(test_df, **params)

        test_res = test_res.copy()
        test_res['equity'] = test_res['equity'] * equity_point

        equity_point= test_res['equity'].iloc[-1]
        results.append(test_res)

    if not results:
        return None
    final_df = pd.concat(results, ignore_index=False)

    return final_df

def main():
    df = pd.read_csv("../data/SBER.csv")
    df['timestamp'] = pd.to_datetime(df['begin'])
    df.set_index('timestamp', inplace=True)
    df = df[['close']]

    result_df = walk_forward_optimization(df, train_month=6, test_month=3, trials=100)
    result_df['equity'].plot()
    plt.show()

    daily_returns = (1 + result_df['strategy_returns']).resample('1D').prod() - 1
    sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252)

    print(sharpe)

if __name__ == "__main__":
    main()