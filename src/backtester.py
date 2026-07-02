import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
import optuna
import matplotlib.pyplot as plt
from src.get_features import add_log_returns, add_volatility, add_drawdown_features
from src.train_hmm import train_hmm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def prepare_x(candles):
    candles = add_log_returns(candles, [1, 7, 14, 30, 90])
    candles = add_volatility(candles, [7, 14, 30, 90])
    candles = add_drawdown_features(candles, [7, 14, 30, 90, 180])

    features = [
        "log_returns_7", "log_returns_14", "log_returns_30", "log_returns_90",
        "volatility_7", "volatility_14", "volatility_30", "volatility_90",
        "drawdown_7", "drawdown_14", "drawdown_30", "drawdown_90", "drawdown_180"
    ]

    candles = candles.dropna()
    x = candles[features].values

    scaler = StandardScaler()
    x = scaler.fit_transform(x)

    pca = PCA()
    x_pca = pca.fit_transform(x)
    evr = pca.explained_variance_ratio_
    n_components = np.argmax(np.cumsum(evr) >= 0.95) + 1
    x = x_pca[:, :n_components]

    return x

def hmm(candles):
    # candles = train_df.resample("D").agg({
    #     'open': 'first',
    #     'high': 'max',
    #     'low': 'min',
    #     'close': 'last',
    #     'volume': 'sum'
    # }).dropna()


    x = prepare_x(candles)
    model = train_hmm(x, n_states=3, n_iter=100)

    return model

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

def backtest(df, model, z_entry, z_exit, z_window):
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

def objective(trial, df, model):
    df = df.copy()

    z_entry = trial.suggest_float('z_entry', 0.0, 5)
    z_exit = trial.suggest_float('z_exit', 0.0, z_entry)
    z_window = trial.suggest_int('z_window', 0, 100)

    df = backtest(df, model, z_entry, z_exit, z_window)

    daily_returns = (1 + df['strategy_returns']).resample('1D').prod() - 1
    sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252)

    return sharpe

def optimize(df, model, trials=200):
    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: objective(trial, df, model), n_trials=trials, n_jobs=-1)

    return study.best_params

def walk_forward_optimization(df, train_month, test_month, trials=200, hmm_use=False):
    df = df.copy()

    windows = generate_walk_forward_windows(df, train_month, test_month)

    results = []
    equity_point = 1.0
    for train_start, train_end, test_start, test_end in windows:
        train_df = df.loc[train_start:train_end].copy()
        test_df = df.loc[test_start:test_end].copy()

        if hmm_use:
            hmm_df = df.loc[df.index[0]:train_end].copy()
            model = hmm(hmm_df)
        else:
            model = None

        params = optimize(train_df, model, trials)

        test_res = backtest(test_df, model, **params)

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

    result_df = walk_forward_optimization(df, train_month=6, test_month=3, trials=10, hmm_use=True)
    result_df['equity'].plot()
    plt.show()

    daily_returns = (1 + result_df['strategy_returns']).resample('1D').prod() - 1
    sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252)

    print(sharpe)

if __name__ == "__main__":
    main()