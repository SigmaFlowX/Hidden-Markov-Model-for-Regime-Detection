import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time
from matplotlib import pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def get_moex_candles(symbol, start_date, end_date, interval=10, market="shares"):
    url = f"https://iss.moex.com/iss/engines/stock/markets/{market}/boards/TQBR/securities/{symbol}/candles.json"
    cur_date = start_date

    if interval == 10:
        delta = 3
    else:
        delta = 0.5
    df = pd.DataFrame()

    session = requests.Session()

    while cur_date < end_date:
        params = {
            "from": cur_date,
            "till": cur_date + timedelta(days=delta),
            "interval": interval
        }
        while True:
            try:
                response = session.get(url, params=params)
                if response.status_code != 200:
                    print(f"Invalid response {response}")
                    time.sleep(5)
                    continue
                break
            except Exception as e:
                print(f"Exception: {e}")
                time.sleep(5)

        data = response.json()

        temp_df = pd.DataFrame(data["candles"]["data"], columns=data["candles"]["columns"])
        df = pd.concat([df, temp_df], ignore_index=True)


        cur_date = cur_date + timedelta(days=delta)
        print(cur_date)

    duplicates_count = df.duplicated(subset=["begin"]).sum()
    df.drop_duplicates(subset=["begin"], inplace=True)
    print("Number of deleted duplicates:", duplicates_count)

    df['timestamp'] = pd.to_datetime(df['begin'])
    df.set_index('timestamp', inplace=True)
    df.drop(columns=['begin'], inplace=True)

    return df

def save_candles_df(df, file_name):
    path = os.path.join(DATA_DIR, file_name)
    df.to_csv(path, index=False)

def main():
    start_date = datetime(2025, 12, 1)
    end_date = datetime(2025, 12, 31)
    ticker = "IMOEX"
    candles = get_moex_candles(ticker, start_date, end_date, interval=10, market="index")

    save_candles_df(candles, f"{ticker}.csv")

    candles = pd.read_csv(os.path.join(DATA_DIR, f"{ticker}.csv"))
    candles['end'] = pd.to_datetime(candles['end'])
    candles.set_index('end', inplace=True)
    candles = candles.resample('1h').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })

    closes = candles['close'].values
    times = candles.index

    plt.plot(times, closes)
    plt.show()

if __name__ == "__main__":
    main()