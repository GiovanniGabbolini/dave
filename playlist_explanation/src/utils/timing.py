"""
Created on Fri Feb 21 2020

@author Giovanni Gabbolini
"""


import time
import datetime


d = {}


def tick(name=""):
    global d
    d[name] = time.time()


def tock(name=""):
    global d
    return str(datetime.timedelta(seconds=time.time()-d[name]))
