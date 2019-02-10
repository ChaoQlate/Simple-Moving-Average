import time

def SMACross(SMAVals, xVals, yVals):
    offset = len(yVals) - len(SMAVals)
    under = [[],[]]
    over = [[],[]]
    for i in range(1, len(SMAVals)):
        flag = None    
        if yVals[i+offset] > SMAVals[i] and yVals[i - 1 + offset] < SMAVals[i - 1]:
            #sma crosses under market price
            if flag == 1:
                print("ERROR", xVals[i + offset])
            flag = 1
            under[0].append(xVals[i + offset])
            under[1].append(yVals[i + offset])
        elif yVals[i + offset] < SMAVals[i] and yVals[i - 1 + offset] > SMAVals[i - 1]:
            #sma crosses over market price
            if flag == 0:
                print("ERROR", xVals[i + offset])
            flag = 0
            over[0].append(xVals[i + offset])
            over[1].append(yVals[i + offset])
    
    return (tuple(under), tuple(over))

def strat(SMAVals, xVals, yVals, amount):
    under, over = SMACross(SMAVals, xVals, yVals)
    if len(under[0]) > len(over[0]):
        under[0].pop()
        under[1].pop()
    elif len(over[0]) > len(under[0]):
        over[0].pop(0)
        over[1].pop(0)
    if under[0][0] > over[0][0]:
        over[0].pop(0)
        over[1].pop(0)
        under[0].pop()
        under[1].pop()
    
    buy = [[],[],[]]
    sell = [[],[],[]]
    for i in range(len(under[0])):
        buy[0].append(under[0][i])
        buy[1].append(under[1][i])
        buy[2].append(amount//under[1][i]//20)
        sell[0].append(over[0][i])
        sell[1].append(over[1][i])
        sell[2].append(amount//under[1][i]//20)
        amount += (amount//under[1][i]//20 * (sell[1][-1] - buy[1][-1]))
    
    print("Amount: ", amount)
    print(list(map(lambda t : time.strftime("%Y %m %d", time.localtime(t)), buy[0])))
    print(list(map(lambda t : time.strftime("%Y %m %d", time.localtime(t)), sell[0])))
    return (buy, sell)