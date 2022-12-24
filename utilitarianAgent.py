import random
from turtle import forward
import numpy as np
from ethicalAgent import ethicalAgent
from miscFunctions import softmax
class utilitarianAgent(ethicalAgent):

    def __init__(self, attrs={}):
        super().__init__("Utilitarian", attrs)

    def forwardMessage(self, source, dest):
        # self.msgRecvFrom[source] += 1
        forwardUtility = self.msgUtility - self.msgCost
        dropUtility = - self.msgUtility
        forwardProb = softmax([forwardUtility, dropUtility])[0]
        if(random.random() < forwardProb): #Forward message
            self.msgSentInter[dest] += 1
            self.msgForwardedOf[source] += 1
            return True
        else:
            return False

    def isStable(self, prevState):
        return 1
