import pandas as pd
import numpy as np
import helpers

#Første dato
K_slash = 2000 * 365 + 1 * 30 + 2


def organize_data(filename):
    #Sorting the data string from data.py
    with open(filename, "r") as readfile:
        data = readfile.read()
        rows = data.split("\n")
        rows = [element.rstrip("\t").split("\t") for element in rows]

    first_date = rows[-1][0].split(".")
    # print("\nfirst date: ", first_date)
    d0, m0, y0 = int(first_date[0]), int(first_date[1]), int(first_date[2])
    K = helpers.const_K(d0, m0, y0)
    days   = [helpers.date_to_day(row[0], K) for row in rows]
    prices = [float(row[4]) for row in rows]
    days = np.array(days)
    prices = np.array(prices)
    price0 = prices[-1]

    return days, prices, K, price0



def make_array_from_data(filename):
    df = pd.read_csv(filename, header=None)
    dates = df[0].to_numpy()
    prices = df[1].to_numpy()
    days = [date_to_day_slash(element, K_slash) for element in dates]
    prices = [float(element.replace(",", "")) for element in prices]
    return days, prices

     
               
def date_to_day_slash(date, K):
    #Format: (mm/dd/yyyy)
    l = date.split(sep="/")
    l = [element.strip('"') for element in l]
    d_i = l[1].lstrip('0')
    m_i = l[0].lstrip('0')
    return int(d_i) + int(m_i)*30 + int(l[2])*365 - K

# make_array_from_data("data/2000-2024.csv")
