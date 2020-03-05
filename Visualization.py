# -*- coding: utf-8 -*-
"""
Module for Visualizing the graph.

networkx handles layout 

matplotlib handles plotting

"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

import OrganizationDataHolder as ODH
import dataGatherer as DG

class Graph:
    highAlpha = 0.9
    lowAlpha = 0.2
    
    def __init__(self,org):
        self.org = org
        self.G = nx.Graph()
        self.memberNodes = []
        self.repoNodes = []
        
        #add all edges, nodes are created automatically, all edges containd in member2repoindex
        for member in org.members:
            memberID = member.getID()
            for reposWorkedOn in org.member2RepoIndex[member.getName()]:
                
                self.G.add_edge(memberID,reposWorkedOn)
        #add topic edges between repos
        for t in org.topics:
            topicSharers = org.topic2Repos[t]
            #check if atleast two repos have the topic, otherwise its hard to draw an edge. 
            if len(topicSharers) >1:
                for i in range(len(topicSharers)):
                    for j in range(i,len(topicSharers)):
                        self.G.add_edge(topicSharers[i],topicSharers[j])
                        
        #collect information on repo vs member nodes for coloring etc.
        for r in org.repos:
            self.repoNodes.append(r.getID())
    
        for m in org.members:
            self.memberNodes.append(m.getID())
            
        #information about relations between edges and nodes for interactive plotting
        self.node2EdgeFinder = {}
        self.highlightedEdges = []
        
    #simpler draw function, not used.    
    def draw(self):
        plt.clf()
        
        self.pos=nx.spring_layout(self.G,iterations  = 200) 
        #self.pos= nx.layout.spectral_layout(self.G)
        self.pos=nx.spring_layout(self.G,k = 1/np.sqrt(self.G.number_of_edges()+self.G.number_of_nodes()),pos = self.pos,iterations  = 200,scale = 100.0 ) 
        nx.draw_networkx_nodes(self.G,self.pos,
                       nodelist=self.repoNodes,
                       node_color='r',with_labels=True)
          
        nx.draw_networkx_nodes(self.G,self.pos,
                       nodelist=self.memberNodes,
                       node_color='b',with_labels=True)
        nx.draw_networkx_edges(self.G,self.pos)
        nx.draw_networkx_labels(self.G,self.pos)
        
        plt.show()
    #calc pos of the nodes, this time by spring model
    def getPos(self):
         
        self.pos=nx.spring_layout(self.G,iterations  = 10) 
        #self.pos= nx.layout.spectral_layout(self.G)
        self.pos=nx.spring_layout(self.G,k = 1/np.sqrt(self.G.number_of_edges()+self.G.number_of_nodes()),pos = self.pos,iterations  = 200,scale = 100.0 ) 
        return self.pos
    
    
    #init the interactive plotting
    def drawInteractive(self):
        
        pos = self.getPos()
        plt.close('all')
          
        self.fig,self.ax = plt.subplots()
        
        x = np.zeros(len(pos))
        y = np.zeros(len(pos))
        
        #coloring nodes
        c = []
        for i in range(len(pos)):
            x[i] = pos[i][0]
            y[i]= pos[i][1]
            if i in self.memberNodes:
                c.append('r')
            else:
                c.append('b')
        #creating and indexing edges:
        for i in self.G.edges:
            x0, y0 =  self.pos[i[0]]
            x1, y1 =  self.pos[i[1]]
            bufferLine = plt.plot([x0,x1],[y0,y1], c = 'k',alpha = Graph.lowAlpha,zorder = 0)
            bufferLine = bufferLine[0]
            
            
            #add edge to first node 
            buffer = []
            
            if i[0] in self.node2EdgeFinder:
                buffer = self.node2EdgeFinder[i[0]]
            
            buffer.append(bufferLine)
            self.node2EdgeFinder[i[0]] = buffer
            
            #add edge to second node 
            buffer = []
            if i[1] in self.node2EdgeFinder:
                buffer = self.node2EdgeFinder[i[1]]
            
            buffer.append(bufferLine)
            self.node2EdgeFinder[i[1]] = buffer
            
            
        self.scatterPlot = plt.scatter(x,y,c = c,zorder = 1)

        #init ref to annotation text
        self.annot = self.ax.annotate("test", xy=(0,0), xytext=(30,30),textcoords="offset points",
                                 bbox=dict(boxstyle="round"),
                                 arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        
        #event listner
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        
        
        plt.show()
    
    def setAlphaForEdges(self,index):
        for edge in self.node2EdgeFinder[index]:
            edge.set_alpha(Graph.highAlpha)
            self.highlightedEdges.append(edge)
    
    def resetAlphaForHighlightedEdges(self):
        for edge in self.highlightedEdges:
            edge.set_alpha(Graph.lowAlpha)
        self.highlightedEdges = []

    def update_annot(self,ind):
        #text pos
        pos = self.scatterPlot.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        #get node object 
        index = list(ind.keys())
        index = ind[index[0]].tolist()[0]
        node = self.org.number2Node[index]
        
        text = "{} : {}".format(node.getType(),node.getName())
        self.setAlphaForEdges(index)
        self.annot.set_text(text)
        
   
    #on mouse over figure        
    def hover(self,event):
        
        currentlyVisable = self.annot.get_visible()
        #in figure
        if event.inaxes == self.ax:
            
            contains, ind = self.scatterPlot.contains(event)
            #on dot
            if contains:
                
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw()
            else:
                
                if currentlyVisable:
                    self.annot.set_visible(False)
                    self.resetAlphaForHighlightedEdges()
                    self.fig.canvas.draw()
                    
    
#Debug
if __name__ == "__main__":
    #set query 
    Company = "futurice"
    numberOfRepositories = 75# the graph library stops working at too high numbers. :/ 
    numberOfMembersPerRepo = 25 # the graph library stops working at too high numbers. :/ 
    numberOfTopicsPerRepo = 10 
    ''' '''
    query = DG.constructDatarequest(Company,numberOfRepositories,numberOfMembersPerRepo,numberOfTopicsPerRepo)
    response =DG.sendRequest(query)
    print(DG.sendRequest(DG.queryRemainingLimit))
    
    
    org = ODH.Organization(response)
    
    graphObject =  Graph(org)
    
    graphObject.drawInteractive()
