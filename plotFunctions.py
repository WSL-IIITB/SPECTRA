import enum
import numpy as np
import matplotlib.pyplot as plt
from networkFunctions import getNetworkProp
from populationGraph import *
import chart_studio.plotly as py
import copy

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

def plotAsPerType(x, y, ystd, fig, ax, plotType="line"):
    if(plotType=='bar'):
        ax.bar(x,y,yerr=ystd, color=['b','g','r','y'], align='center', alpha=0.5, ecolor='black', capsize=10)
        # ax.text(list(range(len(x))),np.zeros(len(y)),["sample" for _ in range(len(y))])#,[str(val) for val in y])
        for i in range(len(x)):
            ax.text(i,y[i]/2,round(y[i],2),ha = 'center')

    elif(plotType=="line"):
        ax.plot(x,y)
    # plotly_fig = py.plot_mpl(fig,filename="janvi")

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
    plotAsPerType(list(outcomeNetwork.keys()), y_vals, y_stderror, fig, ax, plotType)
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
    color_list = ['darkslateblue','limegreen','firebrick','darkgoldenrod']
    count=0
    fig, ax = plt.subplots()
    for outcome in outcomeDict:
        if(metric=="sum"):
            y_vals = [np.sum(getNetworkProp(outcomeDict[outcome][val].getGraph(), prop)) for val in outcomeDict[outcome]]
        elif(metric=="mean"):
            
            # y_std = [np.std(getNetworkProp(outcomeNetwork[val].getGraph(), prop)) for val in outcomeNetwork]
            # y_stderror = [value/len(y_std) for value in y_std]
            # if(prop=='burnout'or prop=='utility' or prop=='cost'):
            #     y_vals=[np.sum(getNetworkProp(outcomeDict[outcome][val].getGraph(), prop))/(outcomeDict[outcome][val].getNumNodes()*(1-val)) for val in outcomeDict[outcome]]
            # else:
                y_vals = [np.mean(getNetworkProp(outcomeDict[outcome][val].getGraph(), prop)) for val in outcomeDict[outcome]]
        ax.plot(list(outcomeDict[outcome].keys()), y_vals,color=color_list[count])
        count+=1
    if(metric=="mean"):
        # In case of Adv Ratio, uncomment this
        # if(prop=='burnout' or prop=='utility' or prop=='cost'):
        #     y_low = [np.sum(getNetworkProp(transDict[0.1][val].getGraph(),prop))/(transDict[0.1][val].getNumNodes()*(1-val)) for val in transDict[0.1]]
        #     y_high = [np.sum(getNetworkProp(transDict[1][val].getGraph(),prop))/(transDict[1][val].getNumNodes()*(1-val)) for val in transDict[1]]
        y_low = [np.mean(getNetworkProp(transDict[0.1][val].getGraph(), prop)) for val in transDict[0.1]]
        y_high = [np.mean(getNetworkProp(transDict[1][val].getGraph(), prop)) for val in transDict[1]]
    else:
        y_low = [np.sum(getNetworkProp(transDict[0.1][val].getGraph(), prop)) for val in transDict[0.1]]
        y_high = [np.sum(getNetworkProp(transDict[1][val].getGraph(), prop)) for val in transDict[1]]

    ax.fill_between(transDict[0.1].keys(),y_low,y_high,color='#ffe838',alpha=0.25)
    # plotAsPerType(list(outcomeNetwork.keys()), y_vals, y_stderror, ax, plotType)
    # ax.set_xticks(range(len(outcomeNetwork)),list(outcomeNetwork))
    ax.legend(outcomeDict.keys(),ncol=1,bbox_to_anchor=(0.5, 0.75))
    ax.set_xlabel(attr)
    # ax.set_ylabel(prop)
    if(metric=="mean"):
        ax.set_ylabel("Average "+prop)
    else:
        ax.set_ylabel("Total "+prop)
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

def advRatio_shadedPlots(outcomeList,transDict,prop, attr, metric="sum",fig_label='dummy'):
    fig, ax = plt.subplots()
    color_list = ['darkslateblue','limegreen','firebrick','darkgoldenrod']
    count=0
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
            # print(agentDict)
            if metric == "sum":
                for i in agentDict:
                    if(len(agentDict[i]) != 0):
                        agentDict[i] = np.sum([agent.getProperty(prop) for agent in agentDict[i]])
                    else:
                        agentDict[i] = 0
            elif metric == "mean":
                for i in agentDict:
                    if(len(agentDict[i]) != 0):
                        agentDict[i] = np.mean([agent.getProperty(prop) for agent in agentDict[i]])
                    else:
                        agentDict[i] = 0
            # print(agentDict)
            y_vals.append(agentDict[types[0]])
            y_vals_adv.append(agentDict[types[1]])
        ax.plot(list(outcomeList[outcome].keys()), y_vals,color=color_list[count])
        count+=1
    ax.plot(list(outcomeList["Transcendence(0.25)"].keys()), y_vals_adv,color='r')
    ax.legend('Adversary')
    y_vals_trans = []
    for outcome in transDict:
        var = transDict[outcome]
        y_vals = []
        # y_vals_adv = []
        for graph in var:
            types = list(var[graph].getAgentMapping().values())
            G = var[graph].getGraph()
            agentDict = {}
            for i in types:
                agentDict[i] = []
            for agents in G:
                agentType = G.nodes[agents]['agent'].getType()
                agentDict[agentType].append(G.nodes[agents]['agent'])
            if metric == "sum":
                for i in agentDict:
                    if(len(agentDict[i]) != 0):
                        agentDict[i] = np.sum([agent.getProperty(prop) for agent in agentDict[i]])
                    else:
                        agentDict[i] = 0
            elif metric == "mean":
                for i in agentDict:
                    if(len(agentDict[i]) != 0):
                        agentDict[i] = np.mean([agent.getProperty(prop) for agent in agentDict[i]])
                    else:
                        agentDict[i] = 0
            y_vals.append(agentDict[types[0]])
        y_vals_trans.append(y_vals)
            # y_vals_adv.append(agentDict[types[1]])
        # ax.plot(list(outcomeList[outcome].keys()), y_vals)

    ax.fill_between(list(transDict[0.1].keys()),y_vals_trans[0],y_vals_trans[1],color='#ffe838',alpha=0.25)
    list1 = list(outcomeList.keys())
    list1.append("Adversary") 
    ax.legend(list1)
    ax.set_xlabel("Adversary Ratio")
    if metric == "sum":
        ax.set_ylabel("Total "+attr)
    elif metric == "mean":
         ax.set_ylabel("Average "+attr)
    fig.savefig("results/"+fig_label+".png", dpi=600)

def plot_bar(agentDict, prop):
    types = list(agentDict.keys())
    propDict = {}
    for i in agentDict:
        propDict[i] = np.mean([agent.getProperty(prop) for agent in agentDict[i]])
    print(propDict)
    print("type ", types)
    plt.bar(types,list(propDict.values()),color=['b','g','r','y'], align='center', alpha=0.5, ecolor='black', capsize=10)
    y = list(propDict.values())
    for i in range(len(types)):
        plt.text(i,y[i]/2,round(y[i],2),ha = 'center')
    plt.xlabel("Type of Ethical Agent")
    plt.ylabel("Total " + prop)

def plotShaded(rangeDict, prop, attr, legend_title, fig_label="dummy",metric="sum",color='#ffe838'):
    fig, ax = plt.subplots()
    keys_list = list(rangeDict.keys())
    if(metric=="mean"):
        y_low = [np.mean(getNetworkProp(rangeDict[keys_list[0]][val].getGraph(), prop)) for val in rangeDict[keys_list[0]]]
        y_med = [np.mean(getNetworkProp(rangeDict[keys_list[1]][val].getGraph(), prop)) for val in rangeDict[keys_list[1]]]
        y_high = [np.mean(getNetworkProp(rangeDict[keys_list[2]][val].getGraph(), prop)) for val in rangeDict[keys_list[2]]]
    else:
        y_low = [np.sum(getNetworkProp(rangeDict[keys_list[0]][val].getGraph(), prop)) for val in rangeDict[keys_list[0]]]
        y_med = [np.sum(getNetworkProp(rangeDict[keys_list[1]][val].getGraph(), prop)) for val in rangeDict[keys_list[1]]]
        y_high = [np.sum(getNetworkProp(rangeDict[keys_list[2]][val].getGraph(), prop)) for val in rangeDict[keys_list[2]]]
    ax.plot(list(rangeDict[keys_list[0]].keys()),y_low)
    ax.plot(list(rangeDict[keys_list[1]].keys()),y_med)
    ax.plot(list(rangeDict[keys_list[2]].keys()),y_high)
    ax.fill_between(rangeDict[keys_list[0]].keys(),y_low,y_high,color=color,alpha=0.25)
    ax.legend(rangeDict.keys(),ncol=1,bbox_to_anchor=(0.5, 0.75),title=legend_title)
    # plotAsPerType(list(outcomeNetwork.keys()), y_vals, y_stderror, ax, plotType)
    # ax.set_xticks(range(len(outcomeNetwork)),list(outcomeNetwork))
    ax.set_xlabel(attr)
    # ax.set_ylabel(prop)
    if(metric=="mean"):
        ax.set_ylabel("Average "+prop)
    else:
        ax.set_ylabel("Total "+prop)
    fig.savefig("results/"+fig_label+".png", dpi=600)

def advShaded(rangeDict, prop, attr, legend_title, fig_label="dummy",metric="sum",color='#ffb5af'):
    fig, ax = plt.subplots()
    # color_list = ['darkslateblue','limegreen','firebrick','darkgoldenrod']
    # count=0
    list_keys = list(rangeDict.keys())
    y_valsDict = []
    y_advDict = []
    for outcome in rangeDict:
        # print(outcom  e)
        var = rangeDict[outcome]
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
            # print(agentDict)
            if metric == "sum":
                for i in agentDict:
                    if(len(agentDict[i]) != 0):
                        agentDict[i] = np.sum([agent.getProperty(prop) for agent in agentDict[i]])
                    else:
                        agentDict[i] = 0
            elif metric == "mean":
                for i in agentDict:
                    if(len(agentDict[i]) != 0):
                        agentDict[i] = np.mean([agent.getProperty(prop) for agent in agentDict[i]])
                    else:
                        agentDict[i] = 0
            print(agentDict)
            y_vals.append(agentDict[types[0]])
            y_vals_adv.append(agentDict[types[1]])
        y_valsDict.append(y_vals)
        y_advDict.append(y_vals_adv)
    ax.plot(list(rangeDict[list_keys[0]]), y_valsDict[0])
    ax.plot(list(rangeDict[list_keys[1]]), y_valsDict[1])
    ax.plot(list(rangeDict[list_keys[2]]), y_valsDict[2])
    ax.fill_between(list(rangeDict[list_keys[1]]), y_valsDict[0], y_valsDict[2],color=color,alpha=0.25)
    ax.plot(list(rangeDict[list_keys[1]]), y_advDict[1],color='r')
    list_new = copy.deepcopy(list(rangeDict.keys()))
    list_new.append("Adversary ("+ str(list_keys[1])+ ")")
    ax.legend(list_new,ncol=1,title=legend_title)
    ax.set_xlabel("Adversary Ratio")
    if metric == "sum":
        ax.set_ylabel("Total "+attr)
    elif metric == "mean":
         ax.set_ylabel("Average "+attr)
    fig.savefig("results/"+fig_label+".png", dpi=600)