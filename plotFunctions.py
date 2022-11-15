import enum
import numpy as np
import matplotlib.pyplot as plt
from networkFunctions import getNetworkProp
from populationGraph import *

def plotAgentwiseProp(G, prop, plotMean = False, plotType = 'line', ax = None, label = None, color=None):
    numNodes = len(G.nodes())
    propertyValues = getNetworkProp(G, prop)
    if "NA" not in propertyValues:
        if ax == None:
            plt.xticks(range(numNodes))
            if(plotType=='stem'):
                _,_,baseline = plt.stem(range(numNodes), propertyValues, use_line_collection=False)
                plt.setp(baseline, visible=False)
            elif(plotType=='line'):
                plt.plot(range(numNodes), propertyValues)
            elif(plotType=='bar'):
                plt.bar(range(numNodes), propertyValues)
            elif(plotType=='scatter'):
                plt.scatter(range(numNodes), propertyValues)
            else:
                print("Not Valid Plot Type")
                return
            plt.xlabel('Agent id')
            plt.ylabel(prop)
            if plotMean:
                mean = np.mean(propertyValues)
                plt.plot(np.ones(np.shape(propertyValues))*mean)
        else:
            if label == None:
                print("Mulitple Plots without label not allowed")
            else:
                if(plotType=='stem'):
                    if(color != None):
                        ax.stem(range(numNodes), propertyValues, color,markerfmt=color+'o', basefmt=" ", label=label)
                    else:
                        print("Color specification required for multiple stem plots")
                    # ax.setp(baseline, visible=False)
                elif(plotType=='line'):
                    ax.plot(range(numNodes), propertyValues, label=label)
                elif(plotType=='bar'):
                    ax.bar(range(numNodes), propertyValues, label=label)
                elif(plotType=='scatter'):
                    ax.scatter(range(numNodes), propertyValues, label=label)
            if plotMean:
                mean = np.mean(propertyValues)
                ax.plot(np.ones(np.shape(propertyValues))*mean)
    else:
        print("Not applicable property")

def plotAgentWiseVaryParams(outcomeNetwork, prop, attr, plotType="line"):
    _, ax = plt.subplots()
    numNodes = len(list(outcomeNetwork.values())[0].nodes())
    ax.set_xticks(range(numNodes))
    ax.set_xlabel('Agent id')
    ax.set_ylabel(prop)
    colors = ['b','g','r','c','m','y']
    c_ind = 0
    for val in outcomeNetwork:
        if(plotType == 'stem'):
            plotAgentwiseProp(outcomeNetwork[val], prop, ax=ax, label=val, plotType=plotType, color=colors[c_ind%len(colors)])
            c_ind += 1
        else:
            plotAgentwiseProp(outcomeNetwork[val], prop, ax=ax, label=val, plotType=plotType)
    if(plotType=='stem'):
        ax.plot(range(numNodes), np.zeros(numNodes), 'k')
    ax.set_title("Varying "+attr)
    ax.legend()

def plotAsPerType(x, y, ystd, ax, plotType="line"):
    if(plotType=='bar'):
        ax.bar(x,y,yerr=ystd, color=['b','g','r','y'], align='center', alpha=0.5, ecolor='black', capsize=10)
        # ax.text(list(range(len(x))),np.zeros(len(y)),["sample" for _ in range(len(y))])#,[str(val) for val in y])
        for i in range(len(x)):
            ax.text(i,y[i]/2,y[i],ha = 'center')

    elif(plotType=="line"):
        ax.plot(x,y)

def plotNetworkVaryParams(outcomeNetwork, prop, attr, fig_label="dummy",metric="sum", plotType = 'line'):
    print("outcome network ", outcomeNetwork)
    # print([outcomeNetwork[val] for val in range(len(outcomeNetwork))])
    # propertyValues = getNetworkProp(outcomeNetwork, prop)
    y_stderror = np.zeros(len(outcomeNetwork))
    if(metric=="sum"):
        y_vals = [np.sum(getNetworkProp(outcomeNetwork[val].getGraph(), prop)) for val in outcomeNetwork]
    elif(metric=="mean"):
        
        y_vals = [np.mean(getNetworkProp(outcomeNetwork[val].getGraph(), prop)) for val in outcomeNetwork]
        y_std = [np.std(getNetworkProp(outcomeNetwork[val].getGraph(), prop)) for val in outcomeNetwork]
        y_stderror = [value/len(y_std) for value in y_std]
    fig, ax = plt.subplots()
    plotAsPerType(list(outcomeNetwork.keys()), y_vals, y_stderror, ax, plotType)
    # ax.set_xticks(range(len(outcomeNetwork)),list(outcomeNetwork))
    ax.set_xlabel(attr)
    ax.set_ylabel(prop)
    if(metric=="mean"):
        ax.set_title("average "+prop+" by varying "+attr)
    else:
        ax.set_title(metric+" of "+prop+" by varying "+attr)
    fig.savefig("results/"+fig_label+".png", dpi=600)
    return y_vals

def plotComparative(outcomeDict, prop, attr, metric="sum", plotType = 'line'):
    # print("outcome network ", outcomeNetwork)
    # print([outcomeNetwork[val] for val in range(len(outcomeNetwork))])
    # propertyValues = getNetworkProp(outcomeNetwork, prop)
    # y_stderror = np.zeros(len(outcomeNetwork))
    _, ax = plt.subplots()
    for outcome in outcomeDict:
        if(metric=="sum"):
            y_vals = [np.sum(getNetworkProp(outcomeDict[outcome][val].getGraph(), prop)) for val in outcomeDict[outcome]]
        # elif(metric=="mean"):
        #     y_vals = [np.mean(getNetworkProp(outcome[val].getGraph(), prop)) for val in outcome]
            # y_std = [np.std(getNetworkProp(outcomeNetwork[val].getGraph(), prop)) for val in outcomeNetwork]
            # y_stderror = [value/len(y_std) for value in y_std]
        
        ax.plot(list(outcomeDict[outcome].keys()), y_vals)
    # plotAsPerType(list(outcomeNetwork.keys()), y_vals, y_stderror, ax, plotType)
    # ax.set_xticks(range(len(outcomeNetwork)),list(outcomeNetwork))
    ax.legend(outcomeDict.keys())
    ax.set_xlabel(attr)
    ax.set_ylabel(prop)
    ax.set_title(metric+" of "+prop+" by varying "+attr)
    return y_vals

def plotComparativeRes(outcomeDict, attr, metric="sum", plotType = 'line'):
    # print("outcome network ", outcomeNetwork)
    # print([outcomeNetwork[val] for val in range(len(outcomeNetwork))])
    # propertyValues = getNetworkProp(outcomeNetwork, prop)
    # y_stderror = np.zeros(len(outcomeNetwork))
    _, ax = plt.subplots()
    for outcome in outcomeDict:
        if(metric=="sum"):
            y_vals = [outcomeDict[outcome][val].getResilience() for val in outcomeDict[outcome]]
        # elif(metric=="mean"):
        #     y_vals = [np.mean(getNetworkProp(outcome[val].getGraph(), prop)) for val in outcome]
            # y_std = [np.std(getNetworkProp(outcomeNetwork[val].getGraph(), prop)) for val in outcomeNetwork]
            # y_stderror = [value/len(y_std) for value in y_std]
        
        ax.plot(list(outcomeDict[outcome].keys()), y_vals)
    # plotAsPerType(list(outcomeNetwork.keys()), y_vals, y_stderror, ax, plotType)
    # ax.set_xticks(range(len(outcomeNetwork)),list(outcomeNetwork))
    ax.legend(outcomeDict.keys())
    ax.set_xlabel(attr)
    ax.set_ylabel("Resilience")
    ax.set_title("Resilience by varying "+attr)
    return y_vals

def plotComparative_shaded(outcomeDict,transDict,prop, attr, fig_label="dummy",metric="sum", plotType = 'line'):
    # print("outcome network ", outcomeNetwork)
    # print([outcomeNetwork[val] for val in range(len(outcomeNetwork))])
    # propertyValues = getNetworkProp(outcomeNetwork, prop)
    # y_stderror = np.zeros(len(outcomeNetwork))
    fig, ax = plt.subplots()
    for outcome in outcomeDict:
        if(metric=="sum"):
            y_vals = [np.sum(getNetworkProp(outcomeDict[outcome][val].getGraph(), prop)) for val in outcomeDict[outcome]]
        elif(metric=="mean"):
            
            # y_std = [np.std(getNetworkProp(outcomeNetwork[val].getGraph(), prop)) for val in outcomeNetwork]
            # y_stderror = [value/len(y_std) for value in y_std]
            if(prop=='burnout'or prop=='utility' or prop=='cost'):
                y_vals=[np.sum(getNetworkProp(outcomeDict[outcome][val].getGraph(), prop))/(outcomeDict[outcome][val].getNumNodes()*(1-val)) for val in outcomeDict[outcome]]
            else:
                y_vals = [np.mean(getNetworkProp(outcomeDict[outcome][val].getGraph(), prop)) for val in outcomeDict[outcome]]
        ax.plot(list(outcomeDict[outcome].keys()), y_vals)
    if(metric=="mean"):
        # In case of Adv Ratio, uncomment this
        # if(prop=='burnout' or prop=='utility' or prop=='cost'):
        #     y_low = [np.sum(getNetworkProp(transDict[0.1][val].getGraph(),prop))/(transDict[0.1][val].getNumNodes()*(1-val)) for val in transDict[0.1]]
        #     y_high = [np.sum(getNetworkProp(transDict[1][val].getGraph(),prop))/(transDict[1][val].getNumNodes()*(1-val)) for val in transDict[1]]
        # else:
            y_low = [np.mean(getNetworkProp(transDict[0.1][val].getGraph(), prop)) for val in transDict[0.1]]
            y_high = [np.mean(getNetworkProp(transDict[1][val].getGraph(), prop)) for val in transDict[1]]
    else:
        y_low = [np.mean(getNetworkProp(transDict[0.1][val].getGraph(), prop)) for val in transDict[0.1]]
        y_high = [np.mean(getNetworkProp(transDict[1][val].getGraph(), prop)) for val in transDict[1]]
    ax.fill_between(transDict[0.1].keys(),y_low,y_high,color='grey',alpha=0.5)
    # plotAsPerType(list(outcomeNetwork.keys()), y_vals, y_stderror, ax, plotType)
    # ax.set_xticks(range(len(outcomeNetwork)),list(outcomeNetwork))
    ax.legend(outcomeDict.keys())
    ax.set_xlabel(attr)
    ax.set_ylabel(prop)
    if(metric=="mean"):
        ax.set_title("Average "+prop+" by varying "+attr)
    ax.set_title(metric+" of "+prop+" by varying "+attr)
    fig.savefig("results/"+fig_label+".png", dpi=600)
    return y_vals

def ethics_linePlots(outcomeList,prop,attr,metric="sum"):
    _, ax = plt.subplots()
    for outcome in outcomeList:
        # print(outcom  e)
        var = outcomeList[outcome]
        y_vals = []
        y_vals_adv = []
        for graph in var:
            # print(var[graph])
            types = list(var[graph].getAgentMapping().values())
            # print(types)
            G = var[graph].getGraph()
            agentDict = {}
            for i in types:
                agentDict[i] = []
            for agents in G:
                agentType = G.nodes[agents]['agent'].getType()
                agentDict[agentType].append(G.nodes[agents]['agent'])
            for i in agentDict:
                agentDict[i] = np.sum(agent.getProperty(prop) for agent in agentDict[i])
            print(agentDict)
            print("type ", types)
            y_vals.append(agentDict[types[0]])
            y_vals_adv.append(agentDict[types[1]])
        print(outcomeList[outcome].keys(), y_vals)
        ax.plot(list(outcomeList[outcome].keys()), y_vals)
        ax.plot(list(outcomeList[outcome].keys()), y_vals_adv)
        ax.legend(types)