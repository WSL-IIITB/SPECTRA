#Virtue : Reliability
import random
import numpy as np
from ethicalAgent import ethicalAgent
from miscFunctions import *

class virtuousAgent(ethicalAgent):

    def __init__(self, attrs= {}):
        '''
        default values
            virtue Cost = 2*message Cost
            Max Virtue Utility = 2*message utility
        '''
        super().__init__("Virtue", attrs)
        if('virtueChange' in attrs):
            self.virtueChange = attrs['virtueChange']
        else:
            self.virtueChange = 2*self.msgCost
        if('maxVirtueUtility' in attrs):
            self.maxVirtueUtility = attrs['maxVirtueUtility']
        else:
            self.maxVirtueUtility = 2*self.msgUtility
        if('delta' in attrs):
            self.delta = attrs['delta']
        else:
            self.delta = 0.01
        self.virtuePoints=0


    def initNeig(self, neigs):
        super().initNeig(neigs)
        self.virtuePoints = 0
    
    def forwardMessage(self, source, dest):
        self.msgRecvFrom[source] += 1
        cost = self.delta*(self.getNodeCost()-self.getNodeUtility())
        forwardUtility = -cost + min(self.virtueChange, self.maxVirtueUtility-self.virtuePoints)
        if self.virtuePoints <= 0:
            dropUtility = -3*self.virtueChange
        else:
            dropUtility = -self.virtueChange
        forwardProb = softmax([forwardUtility, dropUtility])[0]

        if(random.random() < forwardProb): #Forward message
            self.msgSentTo[dest] += 1
            self.msgForwardedOf[source] += 1
            self.virtuePoints += self.virtueChange
            return True
        else:
            self.virtuePoints -= self.virtueChange
            return False
    
    def getVirtuePoints(self):
        return self.virtuePoints
    
    def getProperty(self, prop):
        if(prop == 'virtuePoints'):
            return self.getVirtuePoints()
        return super().getProperty(prop)

    def isStable(self, prevState):
        return 1
        








         
    

        




