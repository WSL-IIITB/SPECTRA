import random
import networkx as nx
from deonticAgent import deonticAgent
from virtuousAgent import virtuousAgent
from utilitarianAgent import utilitarianAgent
from transcendenceAgent import transcendenceAgent
#graph initialization

def initGraph(G, numNodes, common_attrs, type='Virtue'):

    nodeAttr = {}
    for i in range(numNodes):
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
    nx.set_node_attributes(G, nodeAttr)

    for n in G.nodes():
        neigList = list(G.neighbors(n))
        agent = G.nodes[n]['agent']
        agent.initNeig(neigList)

def createMsgs(numMsg, numNodes, G):
    msgList = []
    n = numNodes-1
    random.seed(2)
    while(len(msgList) < numMsg):
        inter = random.randint(0, n)
        neigList = list(G.neighbors(inter))
        if len(neigList) <= 1:
            continue
        source = random.choice(neigList)
        neigList.remove(source)
        dest = random.choice(neigList)
        msg = [source, inter, dest]
        msgList.append(msg)
    return msgList

def transmitMsgs(msgList, G):
    nf, nd = (0,0)
    for n in G.nodes():
        neigList = list(G.neighbors(n))
        agent = G.nodes[n]['agent']
        agent.initNeig(neigList)
    for m in msgList:
        # print(m)
        s, i, d = m
        source = G.nodes[s]['agent']
        inter = G.nodes[i]['agent']
        dest = G.nodes[d]['agent']
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

def getNetworkProp(G, prop):
    agents = [G.nodes[i]['agent'] for i in G.nodes()]
    return [agent.getProperty(prop) for agent in agents]