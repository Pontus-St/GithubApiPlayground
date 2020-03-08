# -*- coding: utf-8 -*-
'''


change the Github token in the datagatherer file on line 10 to your own


get one at
https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line


or ask Me for my access token



'''
import Visualization

import networkx as nx
import matplotlib as Mplt
import numpy as np
import requests
import sys


import OrganizationDataHolder as ODH
import dataGatherer as DG

if __name__ == "__main__":
    #set query 
    ''' please change the following as you wish and change the Github token in the datagatherer file on line 10 ''' 
    Company = "google"
    numberOfRepositories = 30# 3-100, the graph library stops working at too high numbers. :/ 
    numberOfMembersPerRepo =10 # 3-100, the graph library stops working at too high numbers. :/ 
    numberOfTopicsPerRepo = 10 # 3-100,
    
    #input validation
    numberOfRepositories = max(numberOfRepositories,3)
    numberOfRepositories = min(numberOfRepositories,100)
    
    numberOfMembersPerRepo = max(numberOfMembersPerRepo,3)
    numberOfMembersPerRepo = min(numberOfMembersPerRepo,100)
    
    numberOfTopicsPerRepo = max(numberOfTopicsPerRepo,3)
    numberOfTopicsPerRepo = min(numberOfTopicsPerRepo,100)
    
    print("query for company:{} repos:{} members: {} topics:{}".format(Company,numberOfRepositories,numberOfMembersPerRepo,numberOfTopicsPerRepo))
    queryLimit =DG.sendRequest(DG.queryRemainingLimit)
    print(queryLimit)
    if queryLimit == False:
        print("communication with github not working")
    else:
        
        query = DG.constructDatarequest(Company,numberOfRepositories,numberOfMembersPerRepo,numberOfTopicsPerRepo)
        
        response =DG.sendRequest(query)
        print("communication ok")
        
        org = ODH.Organization(response)
        
        if(org.healthy):
            print("Optimizing positions and plotting")
            graphObject =  Visualization.Graph(org)
        
            graphObject.drawInteractive()
            print("plotting graph")
        else:
            print("query and org constructed not working.")

            print("current {:>10}: {:>10}   Pontus ver: {:>10}".format("networkx",nx.__version__ , "2.3"))
            print("current {:>10}: {:>10}   Pontus ver: {:>10}".format("matplotlib",Mplt.__version__ ,"3.1.1"))
            print("current {:>10}: {:>10}   Pontus ver: {:>10}".format("numpy",np.__version__ , " 1.16.5" ))
            print("current {:>10}: {:>10}   Pontus ver: {:>10}".format("requests",requests.__version__ , "2.22.0" ))
            
            print("Pontus Python: 3.7.4\n")
            print("current Python: ",sys.version)
            
            print("\n running debug query")
            
            q_debug_query = '''{    
                organization(login :"google" ) 
                    {
                    name
                    repositories(first :3)
                        {
                        nodes
                            {
                            name
                            mentionableUsers(first :3)
                                {
                                totalCount 
                                nodes
                                    {
                                    login
                                    } 
                                }
                            
                            repositoryTopics(first:3)
                                {
                                nodes
                                    {
                                    topic
                                        {
                                        name
                                        }
                                    }
                                }
                            }
                        
                        }
                                
                    }    
                
                }
                '''
        
            responseDebug =DG.sendRequest(q_debug_query)
            print(responseDebug)
            ODH.Organization.nodeTracker = 0

            orgDebug = ODH.Organization(responseDebug)
            graphObject =  Visualization.Graph(orgDebug)
        
            graphObject.drawInteractive()