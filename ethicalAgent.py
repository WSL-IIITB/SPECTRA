from abc import abstractclassmethod
import numpy as np

class ethicalAgent(object):
    def __init__(self,type,attrs={}):
        '''
        default values 
            msgUtility = 10
            msgCost = 0.1*msgUtility
            burnoutDrop = 5
            burnoutThreshold = 10*msgCost
        '''
        if('msgUtility' in attrs):
            self.msgUtility = attrs['msgUtility']
        else:
            self.msgUtility = 10
        if('costFactor' in attrs):
            self.msgCost = attrs['costFactor']*self.msgUtility
        else:
            self.msgCost = 0.1*self.msgUtility
        if('burnoutDrop' in attrs):
            self.burnoutDrop = attrs['burnoutDrop']
        else:
            self.burnoutDrop = 5
        if('burnoutThreshold' in attrs):
            self.burnoutThreshold = attrs['burnoutThreshold']
        else:
            self.burnoutThreshold = 10*self.msgCost
        self.type = type
        self.isBurntout = False
        self.burnoutState = 0
        self.burnoutCount = 0
        # self.nodeCost = {}
        # self.nodeUtility = {}
        self.msgSentTo = {}
        self.msgRecvFrom = {}
        self.msgForwardedBy = {}
        self.msgForwardedOf = {}
    
    def initNeig(self, neigs):
        for nei in neigs:
            self.msgSentTo[nei] = 0
            self.msgRecvFrom[nei] = 0
            self.msgForwardedBy[nei] = 0
            self.msgForwardedOf[nei] = 0
        self.isBurntout = False
        self.burnoutState= 0
        self.burnoutCount = 0
    
    def sendMessage(self, inter):
        # self.nodeCost[inter] += self.msgCost
        self.msgSentTo[inter] += 1

    def getType(self):
        return self.type
    
    def getNodeCost(self):
        totalMessagesSent = np.sum(list(self.msgSentTo.values()))
        return totalMessagesSent*self.msgCost
    
    def getNodeUtility(self):
        totalMessagesForwarded = np.sum(list(self.msgForwardedBy.values()))
        totalMessagesDropped = np.sum(list(self.msgSentTo.values()))-np.sum(list(self.msgForwardedBy.values()))-np.sum(list(self.msgForwardedOf.values()))
        return (totalMessagesForwarded-totalMessagesDropped)*self.msgUtility
    
    def getBurnouts(self):
        return self.burnoutCount

    def getDropCount(self): 
        totalMessagesDropped = np.sum(list(self.msgSentTo.values()))-np.sum(list(self.msgForwardedBy.values()))-np.sum(list(self.msgForwardedOf.values()))
        return totalMessagesDropped
    
    def getForwardCount(self):
        totalMessagesForwarded = np.sum(list(self.msgForwardedBy.values()))
        return totalMessagesForwarded

    def getProperty(self, prop):
        if(prop == 'cost'):
            return self.getNodeCost()
        elif(prop == 'utility'):
            return self.getNodeUtility()
        elif(prop == 'burnout'):
            return self.getBurnouts()
        elif(prop == 'drops'):
            return self.getDropCount()
        elif(prop == 'forwards'):
            return self.getForwardCount()
        return "NA"

    def burnoutUpdate(self):
        if(self.burnoutDrop != 0):    
            if(self.isBurntout):
                self.burnoutState += 1
                self.burnoutState %= self.burnoutDrop
                if(self.burnoutState == 0):
                    self.isBurntout = False
            else:
                if(self.getNodeCost() >= (1+self.burnoutCount)*self.burnoutThreshold):
                    self.isBurntout = True
                    self.burnoutCount += 1
                    self.burnoutState = 1
        return self.isBurntout

    def sendOutcome(self, inter, sent):
        if sent:
            self.msgForwardedBy[inter] += 1

    @abstractclassmethod
    def forwardMessage(self, source , dest):
        pass

    @abstractclassmethod
    def isStable(self, previousState):
        pass