from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import requests
import pprint as pp

run_main = 1

file = "osebx_data.txt"

#main 
def main(): 
    days, prices, K, price0 = organize_data(file)
    this_price = inputter()
    this_day = date_to_day(get_today_date(), K)
    print_result(this_price, this_day, price0)
    plotter(days, prices, this_day, this_price, price0)

#functions
def get_today_date():
    today_date = datetime.today()
    formatted_date = today_date.strftime('%d.%m.%Y')
    return formatted_date

def get_todays_price():
    url = "https://finance.yahoo.com/quote/OSEBX.OL/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        target_element = soup.find('span', id='data-value')
        if target_element:
            # Extract the value from the element
            value = target_element.text.strip()
            print("Scraped value:", value)
        else:
            print("Target element not found")
    else:
        print("Failed to retrieve the web page")

def functions(x, price0):
    a = price0 * 1.10 ** (x/365)
    b = price0 * 1.09 ** (x/365)
    c = price0 * 1.08 ** (x/365)
    return [a, b, c]

def date_to_day(date, K):
    #Format: (dd.mm.yyyy)
    l = date.split(sep=".")
    d_i = l[0].lstrip("0")
    m_i = l[1].lstrip("0")
    return int(d_i) + int(m_i)*30 + int(l[2])*365 - K

def const_K(d0, m0, y0):
    return d0 + m0 * 30 + y0 * 365
 
def inputter():
    #Input from cmd
    print("\nosebx.py\nloading program ...")
    inp = input("input: [osebx price] >>>  ")
    osebx_current_price = int(inp)
    return osebx_current_price

def organize_data(filename):
    #Sorting the data string from data.py
    with open(filename, "r") as readfile:
        data = readfile.read()
        rows = data.split("\n")
        rows = [element.rstrip("\t").split("\t") for element in rows]
        # pp.pprint(rows)

    first_date = rows[-1][0].split(".")
    print("first date: ", first_date)
    d0, m0, y0 = int(first_date[0]), int(first_date[1]), int(first_date[2])
    K = const_K(d0, m0, y0)
    days   = [date_to_day(row[0], K) for row in rows]
    prices = [float(row[4]) for row in rows]
    price0 = prices[-1]

    return days, prices, K, price0

def plotter(x, y, Px, Py, price0):
    labels = ["10% yearly growth", " 9% yearly growth", " 8% yearly growth"]
    t = np.arange(5000)
    plt.figure("OSEBX")
    plt.title("OSEBX 2014-2024")
    plt.ylim([400, 1600])
    plt.scatter(Px, Py, color="red", label="today")
    plt.plot(x, y)
    funcs = functions(t, price0)
    for i, f in enumerate(funcs):
        plt.plot(t, f, label=labels[i])
    plt.legend()
    plt.grid()
    plt.show()

def print_result(price, day, price0):
    advice = ""
    print("\nresults:")
    funcs = functions(day, price0)
    expected_price = round(funcs[1], 1)

    ratio = round((expected_price - price) / expected_price, 5)
    if -0.01 < ratio < 0.01: advice = " Neutral"
    if ratio < -0.01:        advice = " Sell"
    if ratio < -0.03:        advice = " Strong sell" 
    if ratio >  0.01:        advice = " Buy"
    if ratio >  0.03:        advice = " Strong buy" 

    print("    price0         -> ", price0)
    print("    current  price -> ", price)
    print("    expected price -> ", expected_price)
    print("    difference     -> ", round((ratio * -100), 3),  "%")
    print("    advice         -> " + advice)
    print()
    
if run_main: main()




