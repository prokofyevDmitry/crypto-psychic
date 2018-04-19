"""
All functions to calculate indicators values based on a dataset df of this form: 
	      close    high     low    open        time  volumefrom  volumeto
time being a 
"""

"""
funcs calculating indicators for a given id
"""
import numpy as np
import pandas as pd


def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi


def moving_average(values, window):
    weigths = np.repeat(1.0, window) / window
    smas = np.convolve(values, weigths, 'valid')
    return smas  # as a numpy array


def exp_moving_average(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def MACD(x, slow=27, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = exp_moving_average(x, slow)
    emafast = exp_moving_average(x, fast)
    return emaslow, emafast, emafast - emaslow


def typical_price(value):
    """
    return the typical price of a df['H','L','C']
    """

    return (value['H'] + value['L'] + value['C']) / 3


def CCI(values, periods=20):
    # typical price calculation

    tp = values.apply(lambda x: typical_price(x), axis=1).tail()
    print tp
    smatp = moving_average(tp, periods)[-1]

    print smatp

    mean_deviation = (np.absolute(tp.tail()) - np.absolute(smatp)).sum() / periods

    print mean_deviation

    sum = (tp.tail() - smatp) / (0.015 * mean_deviation)
    print sum
    # print sum


def TR(values, periods=14):
    tr = []
    for index, value in values.iterrows():
        if index == 0:
            # for the first value we calculate only diff between curent high and current low
            tr.append(value['H'] - value['L'])
        else:
            cur_high_cur_low = value['H'] - value['L']
            cur_high_prev_low = np.absolute(value['H'] - values.iloc(index - 1)['L'])
            cur_low_prev_low = np.absolute(value['L'] - values.iloc(index - 1)['L'])


def DMI(values, periods=14):
    dmi = response = pd.DataFrame(columns=['+DM', '-DM', '+DI', '-DI'])

    dm_list = []
    for index, value in values.iterrows():
        dm_dict = {}
        if index > 0:
            up_move = value['H'] - values.iloc(index - 1)['H']
            down_move = values.iloc(index - 1)['L'] - value['L']
            if up_move > down_move and up_move > 0:
                dm_dict['+DM'] = up_move
            else:
                dm_dict['+DM'] = 0
            if down_move > up_move and down_move > 0:
                dm_dict['-DM'] = up_move
            else:
                dm_dict['-DM'] = down_move

            dm_list.append(dm_dict)


response = pd.DataFrame(value)
response[['C', 'H', 'L', 'O']] = response[['C', 'H', 'L', 'O']].apply(pd.to_numeric)

CCI(response)

# print compute_MACD(prices)
