import matplotlib.pyplot as plt
import numpy as np

def plot_price_with_regimes(prices, dates, regimes):
    colors = ['red', 'green', 'grey', 'black']

    position = 0
    for i in range(1, len(regimes)):
        if regimes[i]!= regimes[i-1]:
            plt.plot(dates[position:i], prices[position:i], color=colors[regimes[i-1] % len(colors)])
        position = i

    plt.plot(dates[position:], prices[position:], color=colors[regimes[-1] % len(colors)])