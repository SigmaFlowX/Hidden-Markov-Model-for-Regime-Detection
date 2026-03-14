import matplotlib.pyplot as plt
import numpy as np

def plot_price_with_regimes(prices, dates, regimes):
    plt.plot(dates, prices)
    for i, regime in enumerate(np.unique(regimes)):
        mask = regimes == regime
        plt.fill_between(dates, prices.min(), prices.max(), where=mask, alpha=0.2, label=f'Regime {regime}')
    plt.legend()
    plt.show()