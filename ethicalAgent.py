from abc import abstractclassmethod


class ethicalAgent(object):
    def __init__(self,type,attrs={}):
        if('msgUtility' in attrs):
            self.msgUtility = attrs['msgUtility']
        else:
            self.msgUtility = 10
        if('costFactor' in attrs):
            self.msgCost = attrs['costFactor']*self.msgUtility
        else:
            self.msgCost = 0.1*self.msgUtility
        self.type = type
        # self.nodeCost = {}
        # self.nodeUtility = {}
        self.msgSentTo = {}
        self.msgRecvFrom = {}
        self.msgForwardedBy = {}
    
    def initNeig(self, nei):
        self.msgSentTo[nei] = 0
        self.msgRecvFrom[nei] = 0
        self.msgForwardedBy[nei] = 0
    
    def sendMessage(self, inter):
        # self.nodeCost[inter] += self.msgCost
        self.msgSentTo[inter] += 1

    @abstractclassmethod
    def sentOutcome(self, inter, sent):
        pass

    @abstractclassmethod
    def forwardMessage(self, source , dest):
        pass

    @abstractclassmethod
    def isStable(self, previousState):
        pass