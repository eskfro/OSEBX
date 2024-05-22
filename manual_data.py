import numpy as np
from datetime import datetime

def get_manual_data():
    #[day, price]
    #<--- Newest element first <----
    manual_data = np.array([
        [3667, 1425], [3664, 1417], [3662, 1417], [3661, 1410], [3659, 1416]
    ])

    manual_days, manual_prices = np.hsplit(manual_data, 2)
    manual_days = manual_days.flatten()
    manual_prices = manual_prices.flatten()

    return manual_days, manual_prices

if __name__ == "__main__": 
        get_manual_data()