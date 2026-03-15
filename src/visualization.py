import matplotlib.pyplot as plt
import numpy as np

def plot_price_with_regimes(prices, dates, regimes):
    colors = [
        'green',
        'red',
        '#2ca02c',
        '#d62728',
        '#9467bd',
        '#8c564b',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf',
        '#393b79',
        '#637939',
        '#8c6d31',
        '#843c39',
        '#7b4173',
        '#3182bd',
        '#31a354',
        '#756bb1',
        '#636363',
        '#e6550d'
    ]

    plt.figure(figsize=(8, 4))
    plt.grid()
    plt.tight_layout()
    plt.title("IMOEX over time with predicted regimes")

    start = 0
    for i in range(1, len(regimes)):
        if regimes[i] != regimes[i-1]:
            plt.plot(dates[start:i], prices[start:i], color=colors[regimes[i-1]])
            start = i-1

    plt.plot(dates[start:], prices[start:], color=colors[regimes[-1]])