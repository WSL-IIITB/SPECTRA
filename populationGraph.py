import random
import networkx as nx
from deonticAgent import deonticAgent
from virtuousAgent import virtuousAgent
from utilitarianAgent import utilitarianAgent
from transcendenceAgent import transcendenceAgent

class populationGraph(object):
    def __init__(self, G, common_attrs, type='Virtue'):
        nodeAttr = {}
        self.numNodes = len(G.nodes())
        for i in range(self.numNodes):
            temp = {}
            type = type.split(" ")[0]
            if(type=='Utilitarian'):
                temp['agent'] = utilitarianAgent(common_attrs)
            elif(type=='Virtue'):
                temp['agent'] = virtuousAgent(common_attrs)
            elif(type=='Deontology'):
                temp['agent'] = deonticAgent(common_attrs)
            elif(type=='Transcendence'):
                temp['agent'] = transcendenceAgent(common_attrs)
            nodeAttr[i] = temp
        self.G = G
        self.msgList = []
        nx.set_node_attributes(self.G, nodeAttr)

        for n in self.G.nodes():
            neigList = list(G.neighbors(n))
            agent = self.G.nodes[n]['agent']
            agent.initNeig(neigList)

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