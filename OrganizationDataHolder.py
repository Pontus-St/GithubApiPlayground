# -*- coding: utf-8 -*-
"""
Module for holding the datastructure and information on the connections between the repos and members 
"""
import dataGatherer as DG

class Organization:
    
    #for indexing members and repos for vizualization 
    nodeTracker =0
    #for visualization
    def setNodeNumber():
        toReturn = Organization.nodeTracker 
        Organization.nodeTracker +=1
        return toReturn

    
    #for visualization
    class Node:
        def __init__(self, name,typeOfNode):
            self.id = Organization.setNodeNumber()
            self.name = name
            self.type = typeOfNode
        def getID(self):
            return self.id
        def getName(self):
            return self.name
        def getType(self):
            return self.type
    
    
    
    def __init__(self,queryResponse):
        self.name = ""
        self.members = []           #list of all members -node object
        self.member2RepoIndex = {}  #map from member name to a list of all repos-index that member is connected to  
        
        self.repos = []             #list of all repos -node object
        self.topic2Repos = {}       #map from topics to repos index about that topic 
        self.topics = []            #list of all topics

        self.number2Node = {}       #listfrom index number to node object  
       
        self.healthy = self.extractRepoData(queryResponse)
        
        
        if(len(self.repos) == 0 or len(self.members)==0):
            self.healthy = False
        if self.healthy:
            print("Organization object construction done ")
        else:
            print("Organization object construction failed!  ")
    #extract relevant data from query response     
    def extractRepoData(self, queryResponse):
        #check expected structure:
        try:
            organization =queryResponse["data"]['organization']
            repos =organization["repositories"]["nodes"]
            #data = repos
            #print(data,"\n",type(data), len(data))
        except Exception as e:
            print("failed to unpack query response - wrong kind of query response given: \n", queryResponse)
            return False
        
        
        #for each repo 
        for r in repos:
            #add repo object to different information container
            repoName = r["name"]
            repoBuffer = Organization.Node(repoName,"Repo")
            self.repos.append(repoBuffer)
            self.number2Node[repoBuffer.getID()] = repoBuffer
            
            
            #for each member in that repo add to information container
            for m in r['mentionableUsers']["nodes"]:
                userName = (m["login"])
                
                #if user is already listed
                if userName in self.member2RepoIndex:
                    buffer = self.member2RepoIndex.get(userName)
                    buffer.append(repoBuffer.getID())
                    self.member2RepoIndex[userName] = buffer
                #New user    
                else:
                    self.member2RepoIndex[userName] = [repoBuffer.getID()]
                    memberbuffer = Organization.Node(userName,"User")
                    self.number2Node[memberbuffer.getID()] = memberbuffer
                    self.members.append(memberbuffer)
                    
                    
            #for each topic in that repo add to information container
            for topic in r['repositoryTopics']['nodes']:
                topicName = topic["topic"]["name"]
                
                #if topic  is already listed
                if topicName in self.topic2Repos:
                    buffer = self.topic2Repos.get(topicName)
                    buffer.append(repoBuffer.getID())
                    self.topic2Repos[topicName] = buffer
                
                #New topic    
                else:
                    self.topic2Repos[topicName] = [repoBuffer.getID()]
                    self.topics.append(topicName)
        return True
            
      
#Debug
if __name__ == "__main__":
    query = DG.constructDatarequest("futurice",100,10,10)
    response =DG.sendRequest(query)
    print(response)
    
    
    org = Organization(response)
    
    for i in org.members:
        print("member: " , i.getName()," ",i.getID())
        
    for i in org.member2RepoIndex:
        print("member to repo: ",i , " " ,org.member2RepoIndex[i])
        
    for i in org.topic2Repos:
        print("topic to repo: ",i, " " ,org.topic2Repos[i])
    print(len(org.topics))
    
    for i in org.number2Node:
        print("node number to node object: ",i, " " ,org.number2Node[i].getName())
    print(len(org.number2Node), " " , (len(org.members) + len(org.repos)))
    
    
    
    
    
    