import pandas as pd

filename = "2000-2024.csv"
#Første dato
K_slash = 2000 * 365 + 1 * 30 + 2
run_main = 0

def main():
    print("\nreader.py : main\n")

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

make_array_from_data(filename)

if run_main: main()