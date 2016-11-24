from collections import Counter

import updatewumpusNowWithRocks
import libWumpusWorld


def findGoldProcess(name, solidList, notSolidList, stack):
    maybePitList = []
    maybeWumpusList = []
    visited = []

    # find gold pos
    while True:
        adjacentCell = updatewumpusNowWithRocks.look_ahead(name)
        [smellFlag, airFlag, goldFlag, currentCell, livingFlag] = libWumpusWorld.getCurrentState(name)

        # add currentCell to visited List
        visited.append(currentCell)
        if currentCell not in solidList:
            solidList.append(currentCell)

        # add facts to current list
        libWumpusWorld.addFactsProcess(adjacentCell, smellFlag, airFlag, maybeWumpusList, maybePitList, solidList,
                                       notSolidList)

        # check current game status
        if goldFlag == 'glitter' or livingFlag == 'dead':
            break

        # next step
        flag = libWumpusWorld.nextStep(name, adjacentCell, visited, solidList, notSolidList, currentCell, stack)

        if flag:
            break
    # pick up gold
    libWumpusWorld.pickUpGold(name, stack)

    return [maybePitList, maybeWumpusList]


def killWumpusProcess(name, maybeWumpusList, solidList, notSolidList, stack):
    # find Wumpus pos
    wumpus_pos = Counter(maybeWumpusList).most_common()
    if len(wumpus_pos) == 0:
        return 'TBD'
    print wumpus_pos
    wumpus_pos = wumpus_pos[0][0]

    # initialize lists
    maybePitList = []
    maybeWumpusList = []
    visited = []

    res = '';

    # find wumpus pos
    while True:
        adjacentCell = updatewumpusNowWithRocks.look_ahead(name)
        [smellFlag, airFlag, goldFlag, currentCell, livingFlag] = libWumpusWorld.getCurrentState(name)

        # add currentCell to visited List
        visited.append(currentCell)
        if currentCell not in solidList:
            solidList.append(currentCell)

        # check stop sign
        if wumpus_pos in adjacentCell:
            # find wumpus, kill it
            shootDirection = libWumpusWorld.getNextDirection(currentCell, wumpus_pos)
            print updatewumpusNowWithRocks.take_action(name, shootDirection)
            print updatewumpusNowWithRocks.take_action(name, 'Shoot')
            shootedState = updatewumpusNowWithRocks.take_action(name, "Left")
            if shootedState[8] == 100 or shootedState[8] == 1100:
                res = wumpus_pos
                break
            else:
                res = 'NotSucceeded'
                break

        # add facts to current list
        libWumpusWorld.addFactsProcess(adjacentCell, smellFlag, airFlag, maybeWumpusList, maybePitList, solidList,
                                       notSolidList)

        # next step
        flag = libWumpusWorld.nextStep(name, adjacentCell, visited, solidList, notSolidList, currentCell, stack)

        if flag:
            res = 'NotFound'

    # after kill step back
    libWumpusWorld.stepBack(name, stack)

    return res


def pitFindProcess(name, PitList, solidList, notSolidList, stack):
    # initialize lists
    maybePitList = []
    maybeWumpusList = []
    visited = []

    # return value
    resSolidList = []
    resNotSolidList = []

    # find pit pos
    while True:
        adjacentCell = updatewumpusNowWithRocks.look_ahead(name)
        [smellFlag, airFlag, goldFlag, currentCell, livingFlag] = libWumpusWorld.getCurrentState(name)

        # add currentCell to visited List
        visited.append(currentCell)
        if currentCell not in solidList:
            solidList.append(currentCell)

        # add facts to current list
        libWumpusWorld.addFactsProcess(adjacentCell, smellFlag, airFlag, maybeWumpusList, maybePitList, solidList,
                                       notSolidList)

        # add value to res Lists
        for cell in adjacentCell:
            if cell in PitList:
                tossDirection = libWumpusWorld.getNextDirection(currentCell, cell)
                print updatewumpusNowWithRocks.take_action(name, tossDirection)
                sign = updatewumpusNowWithRocks.take_action(name, 'Toss')
                if sign == 'Quiet':
                    resNotSolidList.append(cell)
                elif sign == 'Clink':
                    resSolidList.append(cell)
                else:
                    break
                PitList = filter(lambda a: a != cell, PitList)

        # check stop sign
        if len(PitList) == 0:
            break

        # next step
        flag = libWumpusWorld.nextStep(name, adjacentCell, visited, solidList, notSolidList, currentCell, stack)

        if flag:
            break
    # after toss step back
    libWumpusWorld.stepBack(name, stack)

    return [resSolidList, resNotSolidList]

def tryToGetPoint(name, solidList, notSolidList, stack):
    visited = []

    # find gold pos
    while True:
        adjacentCell = updatewumpusNowWithRocks.look_ahead(name)
        [smellFlag, airFlag, goldFlag, currentCell, livingFlag] = libWumpusWorld.getCurrentState(name)

        # add currentCell to visited List
        visited.append(currentCell)
        if currentCell not in solidList:
            solidList.append(currentCell)

        # try to kill wumpus
        pos = libWumpusWorld.tryToKillWumpus(name, smellFlag, adjacentCell, solidList, notSolidList, currentCell)
        solidList.append(pos)

        # check current game status
        if goldFlag == 'glitter' or livingFlag == 'dead':
            break

        # next step
        flag = libWumpusWorld.nextStep(name, adjacentCell, visited, solidList, notSolidList, currentCell, stack)

        if flag:
            break
    # pick up gold
    libWumpusWorld.pickUpGold(name, stack)

    # after toss step back
    libWumpusWorld.stepBack(name, stack)

def tryToDie(name):
    visited = []
    stack = []
    # find gold pos
    while True:
        adjacentCell = updatewumpusNowWithRocks.look_ahead(name)
        currentState = updatewumpusNowWithRocks.take_action(name, "Left")
        if currentState == None:
            break
        currentCell = currentState[5]
        # add currentCell to visited List
        visited.append(currentCell)


        # next step
        flag = libWumpusWorld.nextStep(name, adjacentCell, visited, adjacentCell, [], currentCell, stack)

        if flag:
            break
    # after toss step back
    libWumpusWorld.stepBack(name, stack)