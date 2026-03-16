import matplotlib.pyplot as plt
import numpy as np

def plot_price_with_regimes(prices, dates, regimes):
    colors = [
        'green',
        'red',
        'blue',
        'orange',
        'purple',
        'brown',
        'pink',
        'gray',
        'cyan',
        'magenta',
        '#8B4513',
        '#FF69B4',
        '#00CED1',
        '#FFD700',
        '#4B0082',
        '#FF4500',
        '#2E8B57',
        '#DA70D6',
        '#4682B4',
        '#A52A2A'
    ]

    plt.figure(figsize=(8, 4))
    plt.grid()
    plt.tight_layout()
    plt.title("IMOEX over time with predicted regimes")

    start = 0
    for i in range(1, len(regimes)):
        if regimes[i] != regimes[i-1]:
            plt.plot(dates[start:i], prices[start:i], color=colors[regimes[i-1]], legend=regimes[i-1])
            start = i-1

    plt.plot(dates[start:], prices[start:], color=colors[regimes[-1]])