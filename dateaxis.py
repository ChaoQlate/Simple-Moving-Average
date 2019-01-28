import pyqtgraph as pg
from enum import Enum
import time

class DateAxis(pg.AxisItem):

    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(DateAxis, self).__init__(orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True)

        #below are used in calculating the ticks
        #required to store and evaluate the order of ticks
        self.dateMode = None
        self.dateEnum = Enum("dateEnum", "hour day month year")
        self.dateFmtDict = {
            1 : "%H:%M:%S",
            2 : "%d",
            3 : "%b",
            4 : "%Y"
        }

    #overides the definition in AxisItem
    #calculates the exact spacing of axis ticks on key time measures
    #years, months, days, hours
    #returns a list of tuples
    #   [   (major tick spacing, offset),
    #       (minor tick spacing, offset),
    #       (subminor tick spacing, offset),
    #       ...
    #   ]
    def tickSpacing(self, minVal, maxVal, size):
        # First check for override tick spacing
        if self._tickSpacing is not None:
            return self._tickSpacing
        #returns the 2 max corresponding spacing of time measurements
        levels = []
        dif = abs(maxVal - minVal)

        if dif >= 365 * 24 * 60 * 60:
            levels.append((365 * 24 * 60 * 60, 0))
            self.dateMode = self.dateEnum.year.value

        if dif >= 30 * 24 * 60 * 60:
            levels.append((30 * 24 * 60 * 60, 0))
            self.dateMode = self.dateEnum.month.value if self.dateEnum.month.value > self.dateMode else self.dateMode

        if dif >= 24 * 60 * 60:
            levels.append((24 * 60 * 60, 0))
            self.dateMode = self.dateEnum.day.value if self.dateEnum.day.value > self.dateMode else self.dateMode

        if dif >= 60 * 60:
            levels.append((60 * 60, 0))
            self.dateMode = self.dateEnum.hour.value if self.dateEnum.hour.value > self.dateMode else self.dateMode

        while (len(levels) > 2):
            levels.pop()
        
        return levels

    #overrides the definition in AxisItem
    #provides a list of names for specified ticks
    def tickStrings(self, values, scale, spacing):
        strns = []

        if values == []:
            return []
        for val in values:
            strns.append(time.strftime(self.dateFmtDict[self.dateMode], time.localtime(val)))
        self.dateMode -= 1

        label = "Time " + time.strftime("%d-%m-%y", time.localtime(min(values))) + " to " + time.strftime("%d-%m-%y",time.localtime(max(values)))
        self.setLabel(text=label)

        return strns