import updatewumpusNowWithRocks


def getCoordinate(cell):
    res = [];
    res.append(int(cell[5]))  # row number
    res.append(int(cell[6]))  # col number
    return res


def getNextDirection(curCell, nextCell):
    curCoordinate = getCoordinate(curCell)
    nextCoordinate = getCoordinate(nextCell)
    if curCoordinate[0] > nextCoordinate[0]:
        return 'Left'
    elif curCoordinate[0] < nextCoordinate[0]:
        return 'Right'
    elif curCoordinate[1] > nextCoordinate[1]:
        return 'Down'
    elif curCoordinate[1] < nextCoordinate[1]:
        return 'Up'


def getNextDirection_Backward(lastDirection):
    if lastDirection == 'Left':
        return 'Right'
    elif lastDirection == 'Right':
        return 'Left'
    elif lastDirection == 'Down':
        return 'Up'
    elif lastDirection == 'Up':
        return 'Down'
    else:
        return 'Wrong Input'


def addFactsProcess(adjacentCell, smellFlag, airFlag, maybeWumpusList, maybePitList, solidList, notSolidList):
    for cell in adjacentCell:
        if cell in solidList or cell in notSolidList:
            continue
        if smellFlag == 'clean' and airFlag == 'calm':
            solidList.append(cell)
            maybePitList = filter(lambda a: a != cell, maybePitList)
            maybeWumpusList = filter(lambda a: a != cell, maybeWumpusList)
        elif smellFlag != 'clean' and airFlag == 'calm':
            if cell in maybePitList and cell not in maybeWumpusList:
                maybePitList = filter(lambda a: a != cell, maybePitList)
                solidList.append(cell)
            else:
                maybeWumpusList.append(cell)
        elif smellFlag == 'clean' and airFlag != 'calm':
            if cell in maybeWumpusList and cell not in maybePitList:
                maybeWumpusList = filter(lambda a: a != cell, maybeWumpusList)
                solidList.append(cell)
            else:
                maybePitList.append(cell)
        else:
            maybeWumpusList.append(cell)
            maybePitList.append(cell)
    return [maybeWumpusList, maybePitList, solidList, notSolidList]


def nextStep(name, adjacentCell, visited, solidList, notSolidList, currentCell, stack):
    forwardFlag = False;
    for cell in adjacentCell:
        if (cell in visited) or (cell not in solidList) or (cell in notSolidList):
            continue
        forwardFlag = True
        nextDirection = getNextDirection(currentCell, cell)
        # add nextDirection to stack
        stack.append(nextDirection)
        # step forward
        print updatewumpusNowWithRocks.take_action(name, nextDirection)
        print updatewumpusNowWithRocks.take_action(name, "Step")
        break
    if len(stack) == 0:
        return True
    if not forwardFlag:
        # if there is no solid cell near, go backward and the current pos is not the start pos
        nextDirection = getNextDirection_Backward(stack.pop())
        # step backward
        print updatewumpusNowWithRocks.take_action(name, nextDirection)
        print updatewumpusNowWithRocks.take_action(name, "Step")


def pickUpGold(name, stack):
    currentState = updatewumpusNowWithRocks.take_action(name, "Left")
    goldFlag = currentState[2];
    if goldFlag == "glitter":
        # gold finded and back to start pos
        print updatewumpusNowWithRocks.take_action(name, 'PickUp')
        while len(stack) != 0:
            # go backward
            nextDirection = getNextDirection_Backward(stack.pop())
            # step backward
            print updatewumpusNowWithRocks.take_action(name, nextDirection)
            print updatewumpusNowWithRocks.take_action(name, "Step")


def stepBack(name, stack):
    while len(stack) != 0:
        # go backward
        nextDirection = getNextDirection_Backward(stack.pop())
        # step backward
        print updatewumpusNowWithRocks.take_action(name, nextDirection)
        print updatewumpusNowWithRocks.take_action(name, "Step")


def getCurrentState(name):
    currentState = updatewumpusNowWithRocks.take_action(name, "Left")
    smellFlag = currentState[0];
    airFlag = currentState[1];
    goldFlag = currentState[2];
    currentCell = currentState[5];
    livingFlag = currentState[7];
    return [smellFlag, airFlag, goldFlag, currentCell, livingFlag]

def tryToKillWumpus(name, smellFlag, adjacentCell, solidList, notSolidList, currentCell):
    if smellFlag == 'nasty':
        for cell in adjacentCell:
            if cell not in solidList and cell not in notSolidList:
                shootDirection = getNextDirection(currentCell, cell)
                print updatewumpusNowWithRocks.take_action(name, shootDirection)
                print updatewumpusNowWithRocks.take_action(name, 'Shoot')
                return cell