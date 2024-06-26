# from bs4 import BeautifulSoup
# import requests
# from PIL import Image

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import os

from reader import make_array_from_data
from reader import K_slash
from reader import filename

from manual_data import get_manual_data
from manual_data import remove_top_row
from manual_data import add_data

run_main = 1

file = "2014-2024.txt"

#main 
def main(): 
    print("\nosebx.exe\nosebx.py\n\nloading program ...\n")
    printer()
    go = True
    while go:
        #input 
        mode, this_price = inputter()

        #checker
        if mode == -1: continue
        if mode == 0:  return
        
        if (mode != 10 and mode != 24):
            print("error: mode error")
            continue
        else:
            if mode == 10:
                days, prices, K, price0 = organize_data(file)
                manual_days, manual_prices = get_manual_data()
                days = np.concatenate((manual_days, days))
                prices = np.concatenate((manual_prices, prices))
                a, b = exponential_regression(days, prices)
                exp_price0 = exponential_func(0, a, b)
                this_day = days_since_date_new()
                print_result(this_price, this_day, price0, a, b)
                plotter(days, prices, this_day, this_price, exp_price0, a, b, mode)
            else:
                price0 = 143.79
                days, prices = make_array_from_data(filename)
                # manual_days, manual_prices = get_manual_data()
                # days = np.concatenate((manual_days, days))
                # prices = np.concatenate((manual_prices, prices))
                a, b  = exponential_regression(days, prices)
                this_day = date_to_day(get_today_date(), K_slash)
                print_result(this_price, this_day, price0, a, b)
                plotter(days, prices, this_day, this_price, price0, a, b, mode)

#functions
def exponential_func(x, a, b):
        return a * np.exp(b * x)

def get_today_date():
    today_date = datetime.today()
    formatted_date = today_date.strftime('%d.%m.%Y')
    return formatted_date

def days_since_date_new():
    start_date = datetime(2014, 5, 7)
    current_date = datetime.now()
    difference = current_date - start_date
    return difference.days

def print_days_since_date():
        start_date = datetime(2014, 5, 7)
        current_date = datetime.now()
        difference = current_date - start_date
        print(difference.days)


def functions(x, price0):
    d = price0 * 1.11 ** (x/365)
    a = price0 * 1.10 ** (x/365)
    b = price0 * 1.09 ** (x/365)
    c = price0 * 1.08 ** (x/365)
    return [d, a, b, c]

def date_to_day(date, K):
    #Format: (dd.mm.yyyy)
    l = date.split(sep=".")
    d_i = l[0].lstrip("0")
    m_i = l[1].lstrip("0")
    return int(d_i) + int(m_i)*30 + int(l[2])*365 - K

def const_K(d0, m0, y0):
    return d0 + m0 * 30 + y0 * 365

def printer():
    #ui print
    print("-------------------------------------------------")
    print(f"Input       | Day: {days_since_date_new()}")
    print("-------------------------------------------------")
    print()
    print("[enter]     : Quit")
    print("[0]         : Add    price data")
    print("[1]         : Remove price data")
    print("[10 price]  : 10 year plot")
    print("[24 price]  : 24 year plot")
    print()
 
def inputter():
    #Input from cmd

    inp = input(" >>> ")

    if inp == "": return 0, 0

    if len(inp) == 1 and inp.isdigit() == True:
        #0 add price
        if int(inp) == 0: 
            todays_price = input("OSEBX price today [enter to exit] >>> ")
            if todays_price == "":
                return -1, -1
            if len(todays_price) == 4 and todays_price.isdigit():
                add_data(days_since_date_new(), int(todays_price))
            return -1, -1
        
        #1 remove top row
        if int(inp) == 1:
            sure = input("Are you sure you want to delete the latest data? [y/n] >>> ")
            if sure == "y": 
                remove_top_row()
            return -1, -1
    
        return -1, -1
    
    if (len(inp) != 7): 
        return -1, -1
    try:
        inp = inp.split(sep=" ")
        mode = int(inp[0])
        this_price = int(inp[1])
        return mode, this_price
    except ValueError:
        print("Error: Value error")
        return -1, -1
    except IndexError:
        print("Error: Index error")
        return -1, -1

def organize_data(filename):
    #Sorting the data string from data.py
    with open(filename, "r") as readfile:
        data = readfile.read()
        rows = data.split("\n")
        rows = [element.rstrip("\t").split("\t") for element in rows]

    first_date = rows[-1][0].split(".")
    # print("\nfirst date: ", first_date)
    d0, m0, y0 = int(first_date[0]), int(first_date[1]), int(first_date[2])
    K = const_K(d0, m0, y0)
    days   = [date_to_day(row[0], K) for row in rows]
    prices = [float(row[4]) for row in rows]
    days = np.array(days)
    prices = np.array(prices)
    price0 = prices[-1]

    return days, prices, K, price0

def plotter(x, y, Px, Py, price0, a, b, mode):
    delta_x = 1000
    delta_y = 300
    def exponential_func(x, a, b):
        return a * np.exp(b * x)
    
    labels = ["11% yearly growth","10% yearly growth", " 9% yearly growth", " 8% yearly growth"]
    colors = ["red", "green", "green", "red"]

    title = f"OSEBX - {mode} years"
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    plt.title(title)
    plt.xlabel("Days", rotation=0)
    plt.ylabel("Points", rotation=0)

    if mode == 24: 
        t = np.arange(10000)
        plt.ylim([0, 1700])
        plt.xlim([0, 10_000])
    else: 
        t = np.arange(5000)
        plt.xlim([Px - delta_x, Px + 0.5 * delta_x])
        plt.ylim([Py - delta_y, Py + 0.5 * delta_y])

    plt.scatter(Px, Py, color="red", label="today")
    plt.plot(x, y)
    funcs = functions(t, price0)
    for i, f in enumerate(funcs):
        plt.plot(t, f, label=labels[i], color=colors[i])
    plt.plot(t, exponential_func(t, a, b), label="exponential fit", color="magenta")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    plt.savefig(os.path.join(desktop, "figure.png"), format="png")
    # img = Image.open("figure.png")
    # img.show()
    plt.show()

def print_result(price, day, price0, a, b):
    def exponential_func(x, a, b):
        return a * np.exp(b * x)
    
    advice = "None"

    expected_price = exponential_func(day, a, b)
    ratio = round((expected_price - price) / expected_price, 5)

    if -0.01 < ratio < 0.01: advice = " Neutral"
    if ratio < -0.01:        advice = " Sell"
    if ratio < -0.03:        advice = " Strong sell" 
    if ratio >  0.01:        advice = " Buy"
    if ratio >  0.03:        advice = " Strong buy" 
    print("-------------------------------------------------")
    print("Results")
    print("-------------------------------------------------")
    print("~   Price0          -> ", price0)
    print("~   Current  price  -> ", price)
    print("~   Expected price  -> ", int(expected_price))
    print("~   Difference      -> ", round((ratio * -100), 3),  "%")
    print("~   Advice          -> " + advice)
    print()

from scipy.optimize import curve_fit

def exponential_regression(x, y):
    # Define the exponential function
    def exponential_func(x, a, b):
        return a * np.exp(b * x)
    # Fit the exponential function to the data
    popt, _ = curve_fit(exponential_func, x, y, p0=(1.0, 0.0), maxfev=10000)
    # Get the coefficients
    a, b = popt
    # print("a =", a)
    # print("b =", b)
    return a, b

    
if run_main: main()

# def get_todays_price():
#     url = "https://finance.yahoo.com/quote/OSEBX.OL/"
#     response = requests.get(url)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         target_element = soup.find('span', id='data-value')
#         if target_element:
#             # Extract the value from the element
#             value = target_element.text.strip()
#             print("Scraped value:", value)
#         else:
#             print("Target element not found")
#     else:
#         print("Failed to retrieve the web page")



