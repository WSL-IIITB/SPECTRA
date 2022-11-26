import random
import numpy as np
from ethicalAgent import ethicalAgent

class deonticAgent(ethicalAgent):

    def __init__(self, attrs={}):
        '''
        default values
            experience = 10
            learning rate = 0.1
            forwardProb = between 0.5 and 1
        '''
        super().__init__("Deontology",attrs)
        if('experience' in attrs):
            self.experience = attrs['experience']
        else:
            self.experience = 10
        if('forwardProb' in attrs):
            self.forwardProb = attrs['forwardProb']
        else:
            self.forwardProb = 0.75+random.random()/4
        if('learningRate' in attrs):
            self.learningRate = attrs['learningRate']
        else:
            self.learningRate = 0.05
    
    def sendOutcome(self, inter, sent):
        if sent:
            self.msgForwardedBy[inter] += 1
        messagesSent = np.sum(list(self.msgSentSource.values()))
        if messagesSent >= self.experience:
            messagesForwarded = np.sum(list(self.msgForwardedBy.values()))
            self.forwardProb *= (1-self.learningRate)  
            self.forwardProb += self.learningRate*(messagesForwarded/messagesSent)

    def forwardMessage(self, source, dest):
        self.msgRecvFrom[source] += 1
        if(random.random() < self.forwardProb): #Forward message
            self.msgSentInter[dest] += 1
            self.msgForwardedOf[source] += 1
            return True
        else:
            return False

    def getForwardProb(self):
        return self.forwardProb
    
    def getProperty(self, prop):
        if(prop == 'forwardProb'):
            return self.getForwardProb()
        return super().getProperty(prop)

    def isStable(self, previousState):
        if np.absolute(self.forwardProb - previousState.getForwardProb()) < 1e-2:
            return 1
        return 0