import numpy as np
import reader

from io_functions import * 
from manual_data import *
from analysis import * 
from helpers import *


def osebx_10_year(mode, this_price):
    days, prices, K, price0 = reader.organize_data("data/2014-2024.txt")
    manual_days, manual_prices = get_manual_data("data/manual_data.csv")
    days = np.concatenate((manual_days, days))
    prices = np.concatenate((manual_prices, prices))
    a, b = exponential_regression(days, prices)
    exp_price0 = exponential_func(0, a, b)
    this_day = days_since_date_new()
    print_result(this_price, this_day, price0, a, b)
    plotter(days, prices, this_day, this_price, exp_price0, a, b, mode)
    printDottedLines()



def sp_500_10_year(mode, this_price):
    days, prices, K, price0 = reader.organize_data("data/sp500.txt")
    manual_days, manual_prices = get_manual_data("data/manual_data_500.csv")
    #justere nullpunkt eller nokka sånn
    days += 65
    #importing manual data
    days = np.concatenate((manual_days, days))
    prices = np.concatenate((manual_prices, prices))
    a, b = exponential_regression(days, prices)
    exp_price0 = exponential_func(0, a, b)
    this_day = days_since_date_new()
    print_result(this_price, this_day, price0, a, b)
    plotter(days, prices, this_day, this_price, exp_price0, a, b, mode)
    printDottedLines()



def integral_analysis(mode, this_price):
    days, prices, K, price0 = reader.organize_data("data/2014-2024.txt")
    manual_days, manual_prices = get_manual_data("data/manual_data.csv")
    # days, prices, K, price0 = reader.organize_data("data/sp500.txt")
    # manual_days, manual_prices = get_manual_data("data/manual_data_500.csv")
    days = np.concatenate((manual_days, days))
    prices = np.concatenate((manual_prices, prices))
    a, b = exponential_regression(days, prices)
    exp_price0 = exponential_func(0, a, b)
    this_day = days_since_date_new()
    print_result(this_price, this_day, price0, a, b)

    #Sine pattern
    period = 1293
    tops = [464, 1846, 3049, 3049+period]

    plt.figure()
    for s in tops:
        plt.axvline(s, color="black") 

    plt.plot(days, prices)
    plt.plot(days, a * np.exp(b * days), color="magenta")

    integral_difference = integral_indicator(days, prices)
    plt.plot(days, integral_difference + price0, color="black")
    plt.axhline(0 + price0, color="black")
    plt.axhline(-100 + price0, color="green")
    plt.axhline(100 + price0, color="red")

    A, w, Psi = fit_sinusoidal(integral_difference)
    plt.plot(days, A * np.sin(w * days + Psi) + price0)

    _period = 20
    sma, upper_band, lower_band = bollinger_bands(prices, period=_period)
    plt.plot(days + _period+10, sma, color="red")
    plt.plot(days + _period+10, upper_band, color="green")
    plt.plot(days + _period+10, lower_band, color="green")

    plt.grid()
    plt.show()
    printDottedLines()


# def osebx_24_year(mode, this_price):
#     price0 = 143.79
#     days, prices = reader.make_array_from_data("data/2000-2024.csv")
#     # manual_days, manual_prices = get_manual_data()
#     # days = np.concatenate((manual_days, days))
#     # prices = np.concatenate((manual_prices, prices))
#     a, b  = exponential_regression(days, prices)
#     this_day = date_to_day(get_today_date(), reader.K_slash)
#     print_result(this_price, this_day, price0, a, b)
#     plotter(days, prices, this_day, this_price, price0, a, b, mode)
#     printDottedLines()
#     printer()
