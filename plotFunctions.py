import numpy as np
import matplotlib.pyplot as plt
from networkFunctions import getNetworkProp


def plotAgentwiseProp(G, prop, plotMean = False):
    numNodes = len(G.nodes())
    propertyValues = getNetworkProp(G, prop)
    if "NA" not in propertyValues:
        plt.xticks(range(numNodes), range(1, numNodes+1))
        plt.plot(range(numNodes), propertyValues)
        plt.xlabel('Agent id')
        plt.ylabel(prop)
        if plotMean:
            mean = np.mean(propertyValues)
            plt.plot(np.ones(np.shape(propertyValues))*mean)
        
    else:
        print("Not applicable property")