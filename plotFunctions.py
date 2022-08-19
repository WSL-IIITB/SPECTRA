import numpy as np
import matplotlib.pyplot as plt
from networkFunctions import getNetworkProp


def plotAgentwiseProp(G, prop, plotMean = False, ax = None, label = None):
    numNodes = len(G.nodes())
    propertyValues = getNetworkProp(G, prop)
    if "NA" not in propertyValues:
        if ax == None:
            plt.xticks(range(numNodes), range(1, numNodes+1))
            if label == None:
                plt.plot(range(numNodes), propertyValues)
            else:
                plt.plot(range(numNodes), propertyValues, label=label)
            plt.xlabel('Agent id')
            plt.ylabel(prop)
            if plotMean:
                mean = np.mean(propertyValues)
                plt.plot(np.ones(np.shape(propertyValues))*mean)
        else:
            if label == None:
                ax.plot(range(numNodes), propertyValues)
            else:
                ax.plot(range(numNodes), propertyValues, label=label)
            if plotMean:
                mean = np.mean(propertyValues)
                ax.plot(np.ones(np.shape(propertyValues))*mean)
    else:
        print("Not applicable property")

def plotAgentWiseVaryParams(outcomeNetwork, prop, attr):
    _ , ax = plt.subplots()
    numNodes = len(list(outcomeNetwork.values())[0].nodes())
    ax.set_xticks(range(numNodes), range(1, numNodes+1))
    ax.set_xlabel('Agent id')
    ax.set_ylabel(prop)
    for val in outcomeNetwork:
        plotAgentwiseProp(outcomeNetwork[val], prop, ax=ax, label=val)
    ax.set_title("Varying "+attr)
    ax.legend()

def plotNetworkVaryParams(outcomeNetwork, prop, attr, metric="sum"):
    # propertyValues = getNetworkProp(outcomeNetwork, prop)
    if(metric=="sum"):
        y_vals = [np.sum(getNetworkProp(outcomeNetwork[val], prop)) for val in outcomeNetwork]
    elif(metric=="mean"):
        y_vals = [np.mean(getNetworkProp(outcomeNetwork[val], prop)) for val in outcomeNetwork]
    print(list(range(len(outcomeNetwork))),)
    plt.xticks(list(outcomeNetwork.keys()))
    plt.plot(list(outcomeNetwork.keys()), y_vals)
    plt.xlabel(attr)
    plt.ylabel(prop)
    plt.title(metric+" of "+prop+" by varying "+attr)