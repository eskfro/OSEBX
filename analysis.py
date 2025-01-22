import helpers
import numpy as np
from scipy.optimize import curve_fit

def get_moving_average(window_size, prices):
    i = 0
    moving_average = []
    while i < (len(prices) - window_size):
        window_average = np.mean(prices[i:i+window_size])
        moving_average.append(window_average)
        i+=1
    return moving_average



def exponential_regression(x, y):
    popt, _ = curve_fit(helpers.exponential_func, x, y, p0=(1.0, 0.0), maxfev=10000)
    # Get the coefficients
    a, b = popt
    return a, b


def fit_sinusoidal(data):
    t = np.arange(len(data)) 
    initial_guess = [np.std(data) * np.sqrt(2), 2 * np.pi / len(data), 0]
    params, _ = curve_fit(helpers.sinusoidal_model, t, data, p0=initial_guess)
    A, w, Psi = params
    return A, w, Psi



def CalculateRsi(prices, period=14):
    # Calculate price differences
    deltas = np.diff(prices)
    
    # Separate gains and losses
    gains = deltas.clip(min=0)
    losses = -deltas.clip(max=0)
    
    # Calculate the average gain and loss
    avg_gain = np.convolve(gains, np.ones((period,))/period, mode='valid')
    avg_loss = np.convolve(losses, np.ones((period,))/period, mode='valid')
    
    # Calculate the RS (Relative Strength)
    rs = avg_gain / avg_loss
    
    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))
    
    # Pad the RSI array to match the length of the input prices
    rsi = np.concatenate((np.full((period,), np.nan), rsi))
    
    return rsi



def integral_indicator(days, prices):
    AMPLITUDE = 100

    a, b = exponential_regression(days, prices)
    a, b = float(a), float(b)

    days, prices = np.array(days), np.array(prices)
    expReg = a * np.exp(b*days)

    integral_prices = np.zeros(len(days))
    integral_regression = np.zeros(len(days))

    for n in range(len(days) - 1):
        #Trapesmetoden
        integral_prices[n+1] = integral_prices[n] + (days[n+1] - days[n]) * 0.5 * (prices[n] + prices[n+1])
        integral_regression[n+1] = integral_regression[n] + (days[n+1] - days[n]) * 0.5 * (expReg[n] + expReg[n+1])

    difference_array = integral_prices - integral_regression
    max_amplitude = np.max([np.abs(np.min(difference_array)), np.abs(np.max(difference_array))])
    scalar = AMPLITUDE / max_amplitude
    
    return scalar * difference_array



def bollinger_bands(prices, period=20, num_std_dev=2):
    """
    Calculate Bollinger Bands for a given period and number of standard deviations.
    
    :param prices: List or array of prices.
    :param period: The period over which to calculate the SMA and standard deviation.
    :param num_std_dev: The number of standard deviations for the upper and lower bands.
    :return: Tuple of arrays (middle_band, upper_band, lower_band).
    """
    prices = np.array(prices)
    
    # Calculate the Simple Moving Average (SMA)
    sma = np.convolve(prices, np.ones(period), 'valid') / period
    
    # Calculate the rolling standard deviation
    rolling_std_dev = np.array([np.std(prices[i:i+period]) for i in range(len(prices) - period + 1)])
    
    # Calculate the upper and lower bands
    upper_band = sma + (rolling_std_dev * num_std_dev)
    lower_band = sma - (rolling_std_dev * num_std_dev)
    
    # Pad the bands to match the length of the input prices
    sma = np.concatenate((np.full((period-1,), np.nan), sma))
    upper_band = np.concatenate((np.full((period-1,), np.nan), upper_band))
    lower_band = np.concatenate((np.full((period-1,), np.nan), lower_band))
    
    return sma, upper_band, lower_band