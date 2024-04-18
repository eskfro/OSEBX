import numpy as np
import matplotlib.pyplot as plt
import data
d = data.data

#Eskil Aarset Fromholtz

#Start values from 2014
day0   = 28
month0 = 2
year0  = 2014
K = day0 + month0 * 30 + year0 * 365

y0 = 555.7

def functions(x):
    a = y0 * 1.10 ** (x/365)
    b = y0 * 1.09 ** (x/365)
    c = y0 * 1.08 ** (x/365)
    return [a, b]

def date_to_days(date):
    #Format: (dd.mm.yyyy)
    l = date.split(sep=".")
    d_i = l[0].lstrip("0")
    m_i = l[1].lstrip("0")
    return int(d_i) + int(m_i)*30 + int(l[2])*365 - K
    
def inputter():
    #Input from cmd
    print("\nosebx.py\nWelcome\nloading program ...")
    inp = input("input: [dd.mm.yyyy] [space] [osebx price] >>>  ")
    inp = inp.split()
    day = date_to_days(inp[0])
    obx_current_price = int(inp[1])
    print("input: (day, osebx price) =", (day, obx_current_price))
    return day, obx_current_price

def make_data():
    #Sorting the data string from data.py
    rows = d.split('\n')
    clean_rows = []
    for i in range(len(rows)):
        row = rows[i].rstrip("\t")
        clean_rows.append(row)
    rows = []
    for i in range(len(clean_rows)):
        row = clean_rows[i].split(sep="\t")
        rows.append(row)
    days  = [date_to_days(row[0]) for row in rows]
    prices = [float(row[4]) for row in rows]

    return days, prices 

 
def plotter(x, y):
    labels = ["10% yearly growth", " 9% yearly growth", " 8% yearly growth"]
    t = np.arange(5000)
    plt.figure("OSEBX")
    plt.title("OSEBX 2014-2024")
    plt.ylim([400, 1600])
    plt.scatter(this_day, this_price, color="red", label="today")
    plt.plot(x, y)
    funcs = functions(t)
    for i, f in enumerate(funcs):
        plt.plot(t, f, label=labels[i])
    plt.legend()
    plt.grid()
    plt.show()

def result():
    advice = ""
    print("\nresults:")
    funcs = functions(this_day)
    expected_price = round(funcs[1], 1)

    ratio = round((expected_price - this_price) / expected_price, 5)
    if -0.01 < ratio < 0.01: advice = " Neutral"
    if ratio < -0.01:        advice = " Sell"
    if ratio < -0.03:        advice = " Strong sell"
    if ratio >  0.01:        advice = " Buy"
    if ratio >  0.03:        advice = " Strong buy"

    print("    current  price -> ", this_price)
    print("    expected price -> ", expected_price)
    print("    difference     -> ", round((ratio * -100), 3),  "%")
    print("    advice         -> " + advice)
    print()
    
this_day, this_price = inputter()
days, prices = make_data()
result()
plotter(days, prices)





