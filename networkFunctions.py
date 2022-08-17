import random

def createMsgs(numMsg, numNodes, G):
    msgList = []
    n = numNodes-1
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
    for m in msgList:
        s, i, d = m
        source = G.nodes[s]['agent']
        inter = G.nodes[i]['agent']
        dest = G.nodes[d]['agent']

        source.sendMessage(i)
        sent = inter.forwardMessage(s,d)
        source.sendOutcome(i,sent)
        if sent==1:
            nf+=1
        else: 
            nd+=1
    return nf, nd