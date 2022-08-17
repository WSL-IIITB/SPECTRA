import random
import numpy as np
from ethicalAgent import ethicalAgent

class deonticAgent(ethicalAgent):

    def __init__(self, attrs={}):
        '''
        default values
            msgUtility = 10
            msgCost = 0.1*msgUtility
            experience = 10
        '''
        super().__init__("Deontology",attrs)
        if('experience' in attrs):
            self.experience = attrs['experience']
        else:
            self.experience = 10
        if('forwardProb' in attrs):
            self.forwardProb = attrs['forwardProb']
        else:
            self.forwardProb = 0.5+random.random()/2
    
    def sendOutcome(self, inter, sent):
        if sent:
            self.msgForwardedBy[inter] += 1
        messagesSent = sum(self.msgSentTo.values())
        if messagesSent >= self.experience:
            messagesForwarded = sum(self.msgForwardedBy.values())
            self.forwardProb = messagesForwarded/messagesSent

    def forwardMessage(self, source, dest):
        self.msgRecvFrom[source] += 1
        if(random.random() < self.forwardProb): #Forward message
            self.msgSentTo[dest] += 1
            return 1
        else:
            return 0

    def getForwardProb(self):
        return self.forwardProb

    def isStable(self, prevState):
        if np.absolute(self.forwardProb - prevState.getForwardProb()) < 5e-2:
            return 1
        return 0