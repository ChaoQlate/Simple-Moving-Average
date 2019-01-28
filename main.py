import sys
import time
import dateaxis as da
import pyqtgraph as pg
from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (QApplication ,QComboBox ,QDateEdit ,QGridLayout, 
                                QLabel, QLineEdit, QPushButton ,QSpacerItem ,QWidget)
from read import ReadCSV, DiscoverCSV, FetchFirstLast, MinBound, MaxBound


class ApplicationWindow(QWidget):
    def __init__(self, data, parent=None):
        super(ApplicationWindow, self).__init__(parent)

        #initialises an empty graph
        self.graph = pg.PlotWidget(axisItems={'bottom' : da.DateAxis('bottom')})

        #generates the gui for input and output
        inputLayout = self.CreateInputGroup()
        outputLayout = self.CreateOutputGroup()

        #main QGridLayout used to order the widgets
        mainLayout = QGridLayout()

        #formats the position of QWidgets
        mainLayout.addLayout(inputLayout, 0, 0)
        mainLayout.addLayout(outputLayout, 1, 0)
        mainLayout.addWidget(self.graph, 0 , 1, 2, 2)
        mainLayout.setColumnStretch(1, 1)
        mainLayout.setColumnStretch(0, 0)

        self.setLayout(mainLayout)


    # generates a QGridLayout containing input settings
    def CreateInputGroup(self):
        #QCombobox used to pick the csv file to be read
        #initialises the signal and slot mechanism used to change data.values
        csvComboBox = QComboBox()
        csvComboBox.insertPolicy = csvComboBox.InsertAlphabetically
        csvComboBox.addItems(DiscoverCSV())
        csvComboBox.currentIndexChanged[str].connect(lambda v : self.UpdateDateRange(self.GetDateRangeCSV(v), startBox, endBox))
        csvComboBox.currentIndexChanged[str].connect(ApplicationData.csvFile.fset.__get__(data))
        data.csvFile = csvComboBox.currentText()

        #QDateEdit used to interact and change the starting and ending dates
        startBox = QDateEdit()
        startBox.dateChanged.connect(ApplicationData.startDate.fset.__get__(data))
        data.startDate = startBox.date()

        startLabel = QLabel("&Start")
        startLabel.setBuddy(startBox)

        endBox = QDateEdit()
        endBox.dateChanged.connect(ApplicationData.endDate.fset.__get__(data))
        data.endDate = endBox.date()

        endLabel = QLabel("&End")
        endLabel.setBuddy(endBox)

        #initialises the begging and ending dates
        self.UpdateDateRange(self.GetDateRangeCSV(data.csvFile), startBox, endBox)

        #QLineEdit used to interact and change the money used to trade
        amountBox = QLineEdit()
        amountBox.textEdited.connect(ApplicationData.amount.fset.__get__(data))

        amountLabel = QLabel("&Amount")
        amountLabel.setBuddy(amountBox)

        runButton = QPushButton("&Run")
        runButton.clicked.connect(lambda : self.GenerateNewGraph(data))


        #the QGridLayout used to manager the positioning of above widgets
        layout = QGridLayout()

        layout.addWidget(csvComboBox, 0, 0, 1, 4)
        layout.addWidget(startLabel, 1, 0)
        layout.addWidget(startBox, 1, 1)
        layout.addWidget(endLabel, 1, 2)
        layout.addWidget(endBox, 1, 3)
        layout.addWidget(amountLabel, 2, 0)
        layout.addWidget(amountBox, 2, 1)
        layout.addWidget(runButton, 2, 3)

        return layout

    # generates a QGridLayout containing output values
    def CreateOutputGroup(self):
        # TODO display the outputs such as profit and rate of return and other relevant information
        outputLayout = QGridLayout()

        return outputLayout

    # Signals and slots is the mechanism used to connect controller and model
    # When a signal is emitted such as .currentIndexChange
    # connected slots which follow currentIndex.connect(<slot>) are activated

    # These are some of the custom slots used to recieve signals
    # setters in ApplicationData are also slots

    #   #####   #       #####   #####   #####
    #   #       #       #   #     #     #
    #   #####   #       #   #     #     #####
    #       #   #       #   #     #         #
    #   #####   #####   #####     #     #####

    # updates date range from a given csv file
    # *args are the QWidgets requiring date changes
    def GetDateRangeCSV(self, file):
        first, last = FetchFirstLast(file, header=True)
        dateColumn = 0
        minDate = first.split(",")[dateColumn]
        maxDate = last.split(",")[dateColumn]
        minDate = QDate.fromString(minDate, "yyyy-MM-dd")
        maxDate = QDate.fromString(maxDate, "yyyy-MM-dd")
        return (minDate, maxDate)

    # changes the date ranges of QDateTimeEdit classes and subclasses
    def UpdateDateRange(self, dates, *args):
        minDate = min(dates)
        maxDate = max(dates)
        for _QDateTime in args:
            _QDateTime.setDateRange(minDate, maxDate)
    
    # changes the maximum date of QDateTimeEdit classes and subclasses
    def UpdateMaximumDate(self, date, *arg):
        for _QDateTime in args:
            _QDateTime.setMaximumDate(date)

    # changes the min date of QDateTimeEdit classes and subclasses
    def UpdateMinimumDate(self, date, *arg):
        for _QDateTime in args:
            _QDateTime.setMinimumDate(date)

    def GenerateNewGraph(self, data):
        # attempts to gather the date and closing price of selected stock
        # uses the stored start and end dates to set the range of the values
        xVals, yVals = ReadCSV(data.csvFile)
        xStart = time.mktime(time.strptime(data.startDate.toString("yyyyMMdd"), "%Y%m%d"))
        xEnd = time.mktime(time.strptime(data.endDate.toString("yyyyMMdd"), "%Y%m%d"))
        indexStart = MinBound(xVals, xStart)
        indexEnd = MaxBound(xVals, xEnd)

        oldGraphItem = self.graph.getPlotItem()
        oldGraphItem.clear()
        oldGraphItem.plot(x=xVals[indexStart:indexEnd+1], y=yVals[indexStart:indexEnd+1])

        if data.csvFile == 'TSLA.csv':
            oldGraphItem.plot(x=xVals[indexStart:indexEnd+1], y=yVals[indexStart:indexEnd+1], pen='b')
        else:
            oldGraphItem.plot(x=xVals[indexStart:indexEnd+1], y=yVals[indexStart:indexEnd+1], pen='r')

class ApplicationData(object):
    def __init__(self):
        self._startDate = None
        self._endDate = None
        self._amount = None
        self._csvFile = None
        self._plotData = None

    def test(self, val):
        print(val)

    # some setters are used as slots for ApplicationWindow

    @property
    def startDate(self):
        return self._startDate

    @startDate.setter
    def startDate(self, value):
        self._startDate = value

    @property
    def endDate(self):
        return self._endDate
    
    @endDate.setter
    def endDate(self, value):
        self._endDate = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def csvFile(self):
        return self._csvFile

    @csvFile.setter
    def csvFile(self, value):
        self._csvFile = value
    
    @property
    def plotData(self):
        return self._plotData
    
    @plotData.setter
    def plotData(self, value):
        self._plotData = value

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = ApplicationData()
    win = ApplicationWindow(data)
    win.show()
    app.exec_()