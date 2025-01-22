import csv
import numpy as np
import io_functions

#access data
def get_manual_data(_filename):
    #<--- Newest element first <----
    manual_data = np.genfromtxt(_filename, delimiter=";")
    # print(manual_data)
    manual_days, manual_prices = np.hsplit(manual_data, 2)
    manual_days = manual_days.flatten()
    manual_prices = manual_prices.flatten()

    return manual_days, manual_prices



#add data
def add_data(day, price, _filename):
    with open(_filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        data = list(reader)
    # Add the new row at the top
    data.insert(0, [day, price])
    with open(_filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data)
    io_functions.printMessage(f"Successfully added data to {_filename}")
    


#remove data
def remove_top_row(_filename):
    with open(_filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        data = list(reader)
    # Remove the top row
    data.pop(0)
    with open(_filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data)
    io_functions.printMessage(f"Successfully removed data from {_filename}")

    

if __name__ == "__main__": 
        get_manual_data()