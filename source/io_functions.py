import os
import time
import numpy as np
import matplotlib.pyplot as plt

import source.helpers as helpers 
import source.analysis as analysis
import source.manual_data as manual_data

DELAY = 0.03
CONSOLE_WIDTH = 80
VERTICAL_DOT_COUNT = 5

#Moving average window sizes
WINDOW_SIZE_LOWER = 50
WINDOW_SIZE_UPPER = 200


def startup():
    printMessage("osebx.py")
    printDottedLines()
    print_ui()

def exit():
    printMessage("qutting program")
    time.sleep(1)
    printDottedLines()


def plotter(days, prices, Px, Py, price0, a, b, mode):
    delta_x = 365
    delta_y = 250
    
    #labels and colors
    labels = ["11% yearly growth", "10% yearly growth", " 9% yearly growth", " 8% yearly growth"]
    colors = ["yellow", "green", "green", "yellow"]

    #setup
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize = (8, 6))
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Points")

    #osebx 24 year
    if mode == 24: 
        title = "osebx 24 years"
        t = np.arange(10000)
        ax1.set_ylim([0, 1700])
        ax2.set_xlim([0, 10_000])
        growth = [1.11, 1.10, 1.09, 1.08]

    #osebx 10 year
    elif (mode == 10): 
        title = f"osebx 10 year: {Py}"
        t = np.arange(5000, step = 100)
        ax1.set_xlim([Px - delta_x, Px + 0.5 * delta_x])
        ax1.set_ylim([Py - delta_y, Py + 0.5 * delta_y])
        growth = [1.11, 1.10, 1.09, 1.08]
    
    #sp500 10 year
    else:
        delta_y = 1000
        title = "sp500 10 years"
        t = np.arange(5000)
        ax1.set_xlim([Px - delta_x, Px + 0.5 * delta_x])
        ax1.set_ylim([Py - delta_y, Py + 0.5 * delta_y])
        labels = ["12.5% yearly growth","11.5% yearly growth", " 10.5% yearly growth", " 9.5% yearly growth"]
        growth = [1.125, 1.115, 1.105, 1.095]

    #basic plotting
    fig.canvas.manager.set_window_title(title)
    ax1.set_title(title, fontweight='bold')
    ax1.grid(True)
    ax2.grid(True)


    #plot days, prices
    ax1.plot(days, prices)
    #Dagens pris
    ax1.scatter(Px, Py, color="red", label="today")
    #Linje på høyeste punkt
    ax1.axhline(max(prices), color="orange", label=f"ATH = {round(max(prices))}")


    #exponential growth functions
    funcs = helpers.functions(t, price0, growth)
    for i, f in enumerate(funcs):
        ax1.plot(t, f, label=labels[i], color=colors[i])

    #exponential fit
    ax1.plot(t, helpers.exponential_func(t, a, b), label="exponential fit", color="magenta")

    #moving average
    moving_average_lower = analysis.get_moving_average(WINDOW_SIZE_LOWER, prices)
    moving_average_upper = analysis.get_moving_average(WINDOW_SIZE_UPPER, prices)
    low = days[:len(days) - WINDOW_SIZE_LOWER]
    high = days[:len(days) - WINDOW_SIZE_UPPER]

    ax1.plot(low,  moving_average_lower, color="limegreen", label=f"SMA {WINDOW_SIZE_LOWER}")
    ax1.plot(high, moving_average_upper, color="red", label=f"SMA {WINDOW_SIZE_UPPER}")

    #Plotting RSI
    rsi = analysis.CalculateRsi(prices)
    ax2.plot(np.arange(365), rsi[:365])
    ax2.axhline(70, color="red")
    ax2.axhline(30, color="green")
    ax2.set_xlim([0, 365 + 182])
    ax2.set_ylim([0, 100])
    ax2.set_title(f"RSI 14: {round(rsi[364], 1)}", fontweight='bold')
    


    #legend and stuff
    ax1.legend()
    plt.tight_layout()
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop/phinans")
    plt.savefig(os.path.join(desktop, "osebx.png"), format="png")

    plt.show()






def inputter():
    #Input from cmd
    # return -1, -1 to continue loop in main()
    # return  0,  0 to exit     loop in main()

    available_modes = [10, 11, 24, 50]

    inp = input(" >>> ")

    if inp == "" : return 0, None
    if len(inp) == 1 and inp.isdigit():

        #0 add price
        if int(inp) == 0: 
            mode = getInput("Enter mode [10 or 50] >>> ")
            try:
                mode = int(mode)
            except:
                printError("invalid convertion to int")
                return -1, None

            if mode == 10: 
                market = "osebx"
                manual_filename = "data/manual_data.csv"
            elif mode == 50: 
                market = "sp500"
                manual_filename = "data/manual_data_500.csv"
            else:
                printError("mode error")
                return -1, None

            todays_price = getInput(f"{market} price today [enter to exit] >>> ")

            if todays_price == "":
                return -1, None
            
            if len(todays_price) == 4 and todays_price.isdigit():
                manual_data.add_data(helpers.days_since_date_new(), int(todays_price), manual_filename)
            return -1, None
        
        
        #1 remove top row
        if int(inp) == 1:
            mode = getInput("Enter mode [10 or 50] >>> ")

            try: 
                mode = int(mode)
            except: 
                printError("invalid convertion to int")
                return -1, None
            
            if   mode == 10 : _filename = "data/manual_data.csv"
            elif mode == 50 : _filename = "data/manual_data_500.csv"
            else            : 
                printError("mode error")
                return -1, None

            sure = getInput("Are you sure you want to delete the latest data? [y/n] >>> ")
            if sure == "y": manual_data.remove_top_row(_filename)
            return -1, None
    
        return -1, None
    
    if (len(inp) != 7): 
        printError("nonvalid syntax")
        return -1, None
    try:
        inp = inp.split(sep=" ")
        mode = int(inp[0])
        this_price = int(inp[1])
        if mode not in available_modes:
            printError("mode error")
            return -1, None
        else:
            return mode, this_price
    except ValueError:
        printError("value error")
        return -1, None
    except IndexError:
        printError("index error")
        return -1, None

def printMessage(message):
     print()
     print(message)
     print()


def print_result(price, day, price0, a, b):
    advice = "None"
    expected_price = helpers.exponential_func(day, a, b)
    ratio = round((expected_price - price) / expected_price, 5)

    if -0.01 < ratio < 0.01: advice = "Neutral"
    if ratio < -0.01:        advice = "Sell"
    if ratio < -0.03:        advice = "Strong sell" 
    if ratio >  0.01:        advice = "Buy"
    if ratio >  0.03:        advice = "Strong buy" 

    printDelay()
    print_line()
    printDelay("Results")
    print_line()
    printDelay(f"~   Price0          ->  {price0}")
    printDelay(f"~   Current  price  ->  {price} ")
    printDelay(f"~   Expected price  ->  {int(expected_price)}")
    printDelay(f"~   Difference      ->  {round((ratio * -100), 3)} %")
    printDelay(f"~   Advice          ->  {advice}")
    printDelay()
    print_line()
    printDelay()

def print_ui():
    #ui print
    print_line()
    printDelay(f"Input       | Day: {helpers.days_since_date_new()}")
    print_line()
    printDelay()
    printDelay("[enter]     : Quit")
    printDelay("[0]         : Add    price data")
    printDelay("[1]         : Remove price data")
    printDelay("[10 price]  : 10 year (osebx)")
    printDelay("[50 price]  : 10 year (sp500)")
    printDelay()
    print_line()
    printDelay()

def printDelay(text = ""):
    time.sleep(DELAY)
    print(text)

def getInput(message):
    print()
    inp = input(message)
    print()
    return inp

def printError(error):
    print()
    print(f"ERROR: {error}")
    print()

def printDottedLines():
    for i in range(VERTICAL_DOT_COUNT):
        print("   .")
        time.sleep(DELAY)
    print()

def print_line():
    print(CONSOLE_WIDTH * "-")