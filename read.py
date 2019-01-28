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

if __name__ == '__main__':
    a = pg.QtGui.QApplication([])
    g = ReadToGraph(file='TSLA.csv')
    g.show()
    a.exec_()
