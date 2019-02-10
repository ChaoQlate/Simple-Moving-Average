import queue

class SimpleMovingAverage():
    def __init__(self, period=5):
        self.period = period
        self.queue = queue.Queue(period)
    
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