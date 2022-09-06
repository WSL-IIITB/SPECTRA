import random
from turtle import forward
import numpy as np
from ethicalAgent import ethicalAgent
from miscFunctions import softmax

class adversarialAgent(ethicalAgent):

    def __init__(self, attrs={}):
        super().__init__("Adversary", attrs)

    def forwardMessage(self, source, dest):
        forwardProb = random.random()*0.2
        if(random.random() < forwardProb): #Forward message
            self.msgSentTo[dest] += 1
            self.msgForwardedOf[source] += 1
            return True
        else:
            return False

    def isStable(self, prevState):
        return 1
