import csv
import numpy as np
from datetime import datetime

def get_manual_data():
    #<--- Newest element first <----
    manual_data = np.genfromtxt("manual_data.csv", delimiter=";")
    # print(manual_data)
    manual_days, manual_prices = np.hsplit(manual_data, 2)
    manual_days = manual_days.flatten()
    manual_prices = manual_prices.flatten()

    return manual_days, manual_prices


def add_data(day, price):
    with open('manual_data.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        data = list(reader)
    # Add the new row at the top
    data.insert(0, [day, price])
    with open('manual_data.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data)
    print("Successfully added data")

def remove_top_row():
    with open('manual_data.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        data = list(reader)
    # Remove the top row
    data.pop(0)
    with open('manual_data.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data)
    print("Successfully removed data")

if __name__ == "__main__": 
        get_manual_data()