#!/usr/bin/python3
import json
from Map import point
from Map import carmessage

directionStr = ['North','East','South','West']

class trafficDevice():

    __deviceID = -1
    __posX = -1
    __posY = -1

    def __init__(self,x,y,devid):
        self.__posX = x
        self.__posY = y
        self.__deviceID = devid

    def getPosX(self):
        return self.__posX
    def getPosY(self):
        return self.__posY
    def getDeviceID(self):
        return self.__deviceID
    def setPosX(self,x):
        self.__posX = x
    def setPosY(self,y):
        self.__posY = y
    def setDeviceID(self,devid):
        self.__deviceID = devid

class light(trafficDevice):
    __lightRule = -1
    __curCycle = -1

    def __init__(self,x,y,devid,r,trafficmap):
        trafficDevice.__init__(self,x,y,devid)
        self.__lightRule = r
        self.__xLightSignal = 0
        self.__yLightSignal = 1
        trafficmap[x][y].setLightID(devid)
        trafficmap[x][y].setPointLightRule(self.__lightRule)

    def getSignal(self,curcycle):
        if (int(curCycle/self.__lightRule)%2==0):
            #x is green, y is red
            return 1
        else:
            #x is red, y is green
            return 0
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class car(trafficDevice):
    __maxVelocity = 0
    __velocity = 0
    __destPosX = -1
    __destPosY = -1
    __arriveDest = 0
    __curPosInPath = 0
    __carPath = []#item is string as (x,y)
    __mapSize = -1
    __msgList = []

    def __init__(self,x,y,devid,maxv,destx,desty,trafficmap):
        trafficDevice.__init__(self,x,y,devid)
        self.__maxVelocity = maxv
        self.__velocity = 0
        self.__destPosX = destx
        self.__destPosY = desty
        self.__arriveDest = 0
        self.__myMap = trafficmap.copy()
        self.__mapSize = len(self.__myMap[0])
        self.__findCarPath()

    def __findCarPath(self):
        x = self.getPosX()
        y = self.getPosY()
        dist = [[-1 for i in range(self.__mapSize)] for i in range(self.__mapSize) ]
        dist[x][y] = 0
        self.__dfs(x,y,dist)
        #print (dist)
        pathx = self.__destPosX
        pathy = self.__destPosY
        while pathx!=x or pathy!=y:
            if pathy-1>=0 and dist[pathx][pathy-1]==dist[pathx][pathy]-1:
                pathy = pathy-1
            elif pathx+1<self.__mapSize and dist[pathx+1][pathy]==dist[pathx][pathy]-1:
                pathx = pathx+1
            elif pathy+1<self.__mapSize and dist[pathx][pathy+1]==dist[pathx][pathy]-1:
                pathy = pathy+1
            elif pathx-1>=0 and dist[pathx-1][pathy]==dist[pathx][pathy]-1:
                pathx = pathx-1
            else:
                print("Error in finding path")
            self.__carPath.insert(0,str(pathx)+','+str(pathy))
        self.__carPath.append(str(self.__destPosX)+','+str(self.__destPosY))
        print("Car",self.getDeviceID()," path:")
        print(self.__carPath)

    def __dfs(self,x,y,dist):
        #print ("current node:",x,",",y)
        if x==self.__destPosX and y==self.__destPosY:
            #print("arrive")
            return
        for direction in self.__myMap[x][y].getRoadDirecs():
            nextx = 0
            nexty = 0
            if direction==0:
                nextx = x-1
                nexty = y
            elif direction==1:
                nextx = x
                nexty = y+1
            elif direction==2:
                nextx = x+1
                nexty = y
            else:
                nextx = x
                nexty = y-1

            if nextx>=self.__mapSize or nextx<0 or nexty>=self.__mapSize or nexty<0:
                continue
            #print ("next node:",nextx,",",nexty)
            if dist[nextx][nexty]==-1 or dist[nextx][nexty]>dist[x][y]+1:
                dist[nextx][nexty] = dist[x][y]+1
                #print ("dist_",nextx,",",nexty," is ",dist[nextx][nexty])
                self.__dfs(nextx,nexty,dist)

    def getVelocity(self):
        return self.__velocity
    def getDestPosX(self):
        return self.__destPosX
    def getDestPosY(self):
        return self.__destPosY
    def sendMsg(self):
        msg = carmessage(self.getDeviceID(),self.getPosX(),self.getPosY())
        return msg
    def receiveMsg(self,msglist):
        for msg in self.__msgList:
            carx = msg.getMsgCarPosX()
            cary = msg.getMsgCarPosY()
            self.__myMap[carx][cary].clearCarIDs()
        self.__msgList.clear()
        self.__msgList = msglist.copy()
        for msg in self.__msgList:
            carx = msg.getMsgCarPosX()
            cary = msg.getMsgCarPosY()
            self.__myMap[carx][cary].addCarID(msg.getMsgCarID())

        self.__carDecision()

    def __carDecision(self):
        posOfLightAhead = -1
        for i in range(1,self.__maxVelocity+1):
            cordinateStr = self.__carPath[self.__curPosInPath+i]
            posOfComma = cordinateStr.find(',')
            aheadPosX = (int)cordinateStr[0,posOfComma]
            aheadPosY = (int)cordinateStr[posOfComma+1,len(cordinateStr)]





#end
