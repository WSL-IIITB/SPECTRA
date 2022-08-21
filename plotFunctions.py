import numpy as np
import matplotlib.pyplot as plt
from networkFunctions import getNetworkProp


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

def plotAsPerType(x, y, ax, plotType="line"):
    if(plotType=='bar'):
        ax.bar(x,y,color='brg')
    elif(plotType=="line"):
        ax.plot(x,y)
def plotNetworkVaryParams(outcomeNetwork, prop, attr, metric="sum", plotType = 'line'):
    # propertyValues = getNetworkProp(outcomeNetwork, prop)
    if(metric=="sum"):
        y_vals = [np.sum(getNetworkProp(outcomeNetwork[val], prop)) for val in outcomeNetwork]
    elif(metric=="mean"):
        y_vals = [np.mean(getNetworkProp(outcomeNetwork[val], prop)) for val in outcomeNetwork]
    _, ax = plt.subplots()
    plotAsPerType(list(outcomeNetwork.keys()), y_vals, ax, plotType)
    ax.set_xticks(range(len(outcomeNetwork)),list(outcomeNetwork.keys()))
    if(prop=="cost"):
        ax.set_ylim(3,4.5)
    elif(prop=="utility"):
        ax.set_ylim(10,16)
    elif(prop=="burnout"):
        ax.set_ylim(0.15,0.35)
    elif(prop=="forwards"):
        ax.set_ylim(1.4,2.00)
    elif(prop=="drops"):
        ax.set_ylim(.25,.60)
    ax.set_xlabel(attr)
    ax.set_ylabel(prop)
    ax.set_title(metric+" of "+prop+" by varying "+attr)
    return y_vals