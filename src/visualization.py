import matplotlib.pyplot as plt
import numpy as np

def plot_price_with_regimes(prices, dates, regimes):
    colors = ['green', 'red', 'grey', 'black']
    plt.figure(figsize=(8, 4))
    plt.grid()
    plt.tight_layout()

    start = 0
    for i in range(1, len(regimes)):
        if regimes[i] != regimes[i-1]:
            plt.plot(dates[start:i], prices[start:i], color=colors[regimes[i-1]])
            start = i

    plt.plot(dates[start:], prices[start:], color=colors[regimes[-1]])