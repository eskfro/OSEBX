import numpy as np
from datetime import datetime


def exponential_func(x, a, b):
        return a * np.exp(b * x)

def sinusoidal_model(t, A, w, Psi):
    return A * np.sin(w * t + Psi)

def days_since_date_new():
    start_date = datetime(2014, 5, 7)
    current_date = datetime.now()
    difference = current_date - start_date
    return difference.days

def functions(x, price0, growth):
    d = price0 * growth[0] ** (x/365)
    a = price0 * growth[1] ** (x/365)
    b = price0 * growth[2] ** (x/365)
    c = price0 * growth[3] ** (x/365)
    return [d, a, b, c]

def get_today_date():
    today_date = datetime.today()
    formatted_date = today_date.strftime('%d.%m.%Y')
    return formatted_date

def print_days_since_date():
        start_date = datetime(2014, 5, 7)
        current_date = datetime.now()
        difference = current_date - start_date
        print(difference.days)

def date_to_day(date, K):
    #Format: (dd.mm.yyyy)
    l = date.split(sep=".")
    d_i = l[0].lstrip("0")
    m_i = l[1].lstrip("0")
    return int(d_i) + int(m_i)*30 + int(l[2])*365 - K

def const_K(d0, m0, y0):
    return d0 + m0 * 30 + y0 * 365