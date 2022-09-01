import random
import networkx as nx
import numpy as np

class populationGraph(object):
    def __init__(self, G, ratios, agent_types, common_attrs):
        nodeAttr = {}
        if(not self.__validateArgs(ratios, agent_types)):
            print("Invalid ratios or mismatch in number of agent types and number of ratios")
            return
        cumRatio = [ratios[0]]
        for i in range(1, len(ratios)):
            cumRatio.append(ratios[i]+cumRatio[-1])
        self.numNodes = len(G.nodes())
        for i in range(self.numNodes):
            temp = {}
            idx = self.__getSample(cumRatio)
            temp['agent'] = agent_types[idx](common_attrs)
            nodeAttr[i] = temp
        self.G = G
        self.msgList = []
        nx.set_node_attributes(self.G, nodeAttr)

        for n in self.G.nodes():
            neigList = list(G.neighbors(n))
            agent = self.G.nodes[n]['agent']
            agent.initNeig(neigList)

    def __validateArgs(self, ratios, agent_types):
        if(len(ratios) <= 0):
            return False
        if(len(ratios) != len(agent_types)):
            return False
        if(sum(ratios) != 1 and np.array(ratios) > 0):
            return False
        return True
    
    def __getSample(self, cumRatio):
        sample = random.random()
        for idx, val in enumerate(cumRatio):
            if(sample <= val):
                return idx

    def createMsgs(self, numMsg,myseed = 32):
        msgList = []
        n = self.numNodes-1
        random.seed(myseed)
        while(len(msgList) < numMsg):
            inter = random.randint(0, n)
            neigList = list(self.G.neighbors(inter))
            if len(neigList) <= 1:
                continue
            source = random.choice(neigList)
            neigList.remove(source)
            dest = random.choice(neigList)
            msg = [source, inter, dest]
            msgList.append(msg)
            self.msgList = msgList
        return msgList
    
    def transmitMsgs(self):
        nf, nd = (0,0)
        for n in self.G.nodes():
            neigList = list(self.G.neighbors(n))
            agent = self.G.nodes[n]['agent']
            agent.initNeig(neigList)
        for m in self.msgList:
            # print(m)
            s, i, d = m
            source = self.G.nodes[s]['agent']
            inter = self.G.nodes[i]['agent']
            dest = self.G.nodes[d]['agent']
            source.sendMessage(i)
            inter_burntout = inter.burnoutUpdate()
            if(not inter_burntout):
                sent = inter.forwardMessage(s,d)
            else:
                sent = False
            source.sendOutcome(i,sent)
            # print(getNetworkProp(G, 'forwardProb'))
            if sent:
                nf += 1
            else: 
                nd += 1
        return nf, nd

    def getNetworkProp(self,prop):
        agents = [self.G.nodes[i]['agent'] for i in self.G.nodes()]
        return [agent.getProperty(prop) for agent in agents]
    
    
    def getGraph(self):
        return self.G