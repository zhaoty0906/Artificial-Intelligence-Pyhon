# encoding: utf-8
'''
Created on 2016年10月29日

@author: KeWang TianyuZhao Yifei Ge
'''
import updatewumpusNowWithRocks
import impWumpusWorld

# initialize world
# name = updatewumpusNowWithRocks.intialize_my_world("Cell 44", "Cell 42", ["Cell 12", "Cell 22", "Cell 32"])
name = updatewumpusNowWithRocks.intialize_world()

# initialize lists
solidList = []
notSolidList = []
preSolidNum = 0;
preNotSolidNum = 0;

# initial stack
stack = []



# try to find gold position
while True:

    # try to find gold
    [maybePitList, maybeWumpusList] = impWumpusWorld.findGoldProcess(name, solidList, notSolidList, stack)

    print stack
    # try to kill wumpus
    killRes = impWumpusWorld.killWumpusProcess(name, maybeWumpusList, solidList, notSolidList, stack)
    if killRes in maybeWumpusList:
        print killRes + ' : Kill Succeeded'
        solidList.append(killRes)
        maybePitList = filter(lambda a: a != killRes, maybePitList)
    else:
        print killRes

    # game ending flag check
    currentState = updatewumpusNowWithRocks.take_action(name, "Left")
    score = currentState[8];
    if score == 1100:
        updatewumpusNowWithRocks.take_action(name, "Exit")
        break
    else:
        [resSolidList, resNotSolidList] = impWumpusWorld.pitFindProcess(name, maybePitList, solidList, notSolidList, stack)

        for e in resNotSolidList:
            if e not in notSolidList:
                notSolidList.append(e)
        for e in resSolidList:
            if e not in solidList:
                solidList.append(e)

    # check if there are some changes in fact
    if preNotSolidNum == len(notSolidList) and preSolidNum == len(solidList):
        print 'There is a bug here'
        break

    preSolidNum = len(solidList)
    preNotSolidNum = len(notSolidList)

# check whether we win the game, if win or got some points exit, else try to find gold according to current KB
currentState = updatewumpusNowWithRocks.take_action(name, "Left")
score = currentState[8]

if score == 0:
    impWumpusWorld.tryToGetPoint(name, solidList, notSolidList, stack)
    currentState = updatewumpusNowWithRocks.take_action(name, "Left")
    livingFlag = currentState[7];
    score = currentState[8]
    if score == 0 and livingFlag == 'living':
        impWumpusWorld.tryToDie(name)

updatewumpusNowWithRocks.take_action(name, "Exit")
