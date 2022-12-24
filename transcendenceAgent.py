import random
import numpy as np
from ethicalAgent import ethicalAgent
from miscFunctions import *

class transcendenceAgent(ethicalAgent):

    def __init__(self, attrs={}):
        '''
        default values
        '''
        super().__init__("Transcendence", attrs)
        if('gamma' in attrs):
            self.gamma = attrs['gamma'] 
        else:
            self.gamma = 0.5
        if('updateEvery' in attrs):
            self.updateEvery = attrs['updateEvery']
        else:
            self.updateEvery = 50
        if('delta' in attrs):
            self.delta = attrs['delta']
        else:
            self.delta = 0.01
        if('learningRate' in attrs):
            self.learningRate = attrs['learningRate']
        else:
            self.learningRate = 0.07
        self.virtualUtility = {}
        self.distance = {}
        self.firstIter = True
    
    def initNeig(self, neigs):
        super().initNeig(neigs)
        for nei in neigs:
            self.virtualUtility[nei] = 0
        if(self.firstIter):
            for nei in neigs:
                self.distance[nei] = 1
            self.firstIter = False


    def __updateDistances(self):
        sources = list(self.msgForwardedOf.keys())
        inters = list(self.msgForwardedBy.keys())
        costVec = []
        rewardVec = []
        # for nei in neighs:
            # asSource = self.msgSentTo[nei]-
        costVec = [self.msgForwardedOf[source]*self.msgCost for source in sources]
        rewardVec = [self.msgForwardedBy[neig]*self.msgUtility+self.virtualUtility[neig] for neig in inters]
        normCost = softmax(costVec)
        normReward = softmax(rewardVec)

        for itr, nei in enumerate(inters):
            deltaDist = normReward[itr]-normCost[itr]
            if(self.distance[nei]-(self.learningRate*deltaDist)<=0):
                self.distance[nei] = 0
            else:
                self.distance[nei] = self.distance[nei] - (self.learningRate*deltaDist)

    def forwardMessage(self, source, dest):
        # self.msgRecvFrom[source] += 1
        cost = self.delta*(self.getNodeCost()-self.getNodeUtility())+self.msgCost
        d = self.distance[source]
        forwardUtility = (-cost+np.power(self.gamma, d)*self.msgUtility)/(1+np.power(self.gamma, d))
        dropUtility = (-np.power(self.gamma, d)*self.msgUtility)/(1+np.power(self.gamma, d))
        forwardProb = softmax([forwardUtility, dropUtility])[0]

        if(random.random() < forwardProb): #Forward message
            self.msgSentInter[dest] += 1
            self.msgForwardedOf[source] += 1
            self.virtualUtility[source] += np.power(self.gamma, d)*self.msgUtility
            return True
        else:
            self.virtualUtility[source] -= np.power(self.gamma, d)*self.msgUtility
            return False
    
    def epochUpdate(self):
        self.__updateDistances()
        return 
    
    def getDistances(self):
        return self.distance

    def isStable(self, previousState):
        curDist = list(self.distance.values())
        prevDist = list(previousState.getDistances().values())
        for i in range(len(curDist)):
            delta = curDist[i] - prevDist[i]
            if np.absolute(delta) > 49e-3:
                return 0
        return 1