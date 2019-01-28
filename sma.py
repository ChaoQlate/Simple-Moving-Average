from PyQt5.QtCore import QObject 
import pyqtgraph as pg
import numpy as np
import dateaxis as da
import queue
import time
import csv

class SimpleMovingAverage():
    def __init__(self, period=50):
        self.period = period
        self.queue = queue.Queue(period + 1)
    
    def update(self, data):
        if type(data) != type([]):
            data = [data]
        for v in data:
            if type(v) != int and type(v) != float:
                raise TypeError("in sma.update value(s) for data parameter must be int or float")
            try:
                self.queue.put(v, block=False)
            except queue.Full:
                self.queue.get(block=False)
                self.queue.put(v, block=False)
    
    def getAverage(self):
        total = 0
        count = 0
        for elem in list(self.queue.queue):
            total += elem
            count += 1

        return float(total) / count

win = pg.GraphicsWindow(title="Simple Moving Average")
win.resize(1000,600)
a = da.DateAxis(orientation="bottom")
plot = win.addPlot(title="TSLA", axisItems={"bottom" : a})

if isinstance(win, QObject):
    print("yeeet")

sma = SimpleMovingAverage(50)
smaVals = []

xVals = []
yVals = []
with open('TSLA.csv', newline='') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        xVals.append(time.mktime(time.strptime(row[0], "%Y-%m-%d")))
        yVals.append(float(row[2]))

        sma.update(float(row[2]))
        smaVals.append(sma.getAverage())



plot.plot(x=xVals, y=yVals, pen='b')
plot.plot(x=xVals, y=smaVals, pen='r')


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()