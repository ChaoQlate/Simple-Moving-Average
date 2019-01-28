import pyqtgraph as pg
import dateaxis as da
import os
import time
import csv

#read column sniffer

def ReadCSV(file=None):
    try:
        xVals = []
        yVals = []
        with open(file, newline='') as f:
            next(f)
            reader = csv.reader(f)
            for row in reader:
                xVals.append(time.mktime(time.strptime(row[0], "%Y-%m-%d")))
                yVals.append(float(row[2]))
    except:
        xVals = []
        yVals = []
    #graph = pg.PlotItem(x=xVals, y=yVals, axisItems={'bottom' : da.DateAxis('bottom')}, pen='b')
    return (xVals, yVals)
    

def DiscoverCSV(path=os.getcwd()):
    return [f for f in os.listdir(path) if f[-4:] == '.csv']

def FetchFirstLast(file, header=False):
    try:
        with open(file, mode='rb') as f:
            if header == True:
                next(f)
            first = f.readline()
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last = f.readline()
    except:
        return (None, None)
    return (str(first, 'utf-8'), str(last, 'utf-8'))

def BinarySearch(arr, val):
    if len(arr) == 0:
        #print(False, 0)
        return (False, 0)
    mid = int(len(arr) / 2.0 - 0.5)
    if arr[mid] == val:
        #print(True, mid)
        return (True, mid)
    elif arr[mid] < val:
        found, index = BinarySearch(arr[mid+1:], val)
        #print(found, mid + index + 1)
        return (found, mid + index + 1)
    else:
        found, index = BinarySearch(arr[0:mid], val)
        #print(found, mid - (len(arr[0:mid]) - index))
        return (found, mid - (len(arr[0:mid]) - index))

#finds the smallest index in a sorted list that is larger than the given value
def MinBound(arr, val):
    found, index = BinarySearch(arr, val)
    for i in range(3):
        if arr[(index + i) % len(arr)] >= val:
            return (index + i) % len(arr)
    return None

#finds the largest index in sorted list that is smaller than the given value
def MaxBound(arr, val):
    found, index = BinarySearch(arr, val)
    for i in range(3):
        if arr[(index - i) % len(arr)] <= val:
            return (index - i) % len(arr)
    return None
