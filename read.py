import pyqtgraph as pg
import dateaxis as da
import os
import time
import csv

# Returns a list containing data of specified columns ranging from start to end
# Assumes the column for start and end are sorted
# start and end are tuples of size 2 (<column name/number>, <key>)
# if columns are empty returns everything
def ReadCSV(file, header=True, start=None, end=None, columns=[]):
    try:
        with open(file, newline='') as f:
            reader = csv.reader(f)
            line = next(reader)

            if not header:
                if start == None:
                    start = (0, line[0])       
            else:
                if start != None and start[0] in line:
                    start = (line.index(start[0]), start[1])
                if end != None and end[0] in line:
                    end = (line.index(end[0]), end[1])
                line = next(reader)
                if start == None:
                    start = (0, line[0])
            if end == None:
                fill, end = FetchFirstLast(file, header=header)
                end = (0, end.split(",")[0])

            while(line[start[0]] < start[1]):
                line = next(reader)

            results = []            
            if columns == []:
                columns = [i for i in range(len(line))]
                    
            for i in columns:
                results.append([line[i]])
            
            if line[end[0]] < end[1]:
                for line in reader:
                    for i in range(len(columns)):
                        results[i].append(line[columns[i]])
                    if line[end[0]] >= end[1]:
                        break 
    except:
        results = []
    return tuple(results)

def DiscoverCSV(path=os.getcwd()):
    return [f for f in os.listdir(path) if f[-4:] == '.csv']

def ConvertTime(dates):
    secondsAfterEpoch = []
    for date in dates:
        secondsAfterEpoch.append(time.mktime(time.strptime(date, "%Y-%m-%d")))
    return secondsAfterEpoch

def FetchFirstLast(file, header=True):
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

if __name__ == "__main__":
    x, y = ReadCSV("TSLANoHeader.csv", start=(0,"2012-06-30"), end=(0, "2013-06-30"), columns=[0,2])
    print(x, y)