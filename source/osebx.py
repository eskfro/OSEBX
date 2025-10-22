
#CUSTOM FILES
from source.io_functions import * 
from source.helpers import *
import source.modes as modes

def main(): 
    startup()
    while True:
        mode, todays_price = inputter()

        if mode == -1: continue
        if mode == 0:  
            exit()
            return
        
        if mode == 10:
            modes.osebx_10_year(mode, todays_price)
        elif mode == 50:
            modes.sp_500_10_year(mode, todays_price)
        else:
            modes.integral_analysis(mode, todays_price)
            
main()





