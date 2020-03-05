# -*- coding: utf-8 -*-
'''


change the Github token in the datagatherer file on line 10 to your own


get one at
https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line


or ask Me for my access token



'''
import Visualization

import OrganizationDataHolder as ODH
import dataGatherer as DG

if __name__ == "__main__":
    #set query 
    ''' please change the following as you wish and change the Github token in the datagatherer file on line 10 ''' 
    Company = "futurice"
    numberOfRepositories = 75# the graph library stops working at too high numbers. :/ 
    numberOfMembersPerRepo = 25 # the graph library stops working at too high numbers. :/ 
    numberOfTopicsPerRepo = 10 
    ''' '''
    query = DG.constructDatarequest(Company,numberOfRepositories,numberOfMembersPerRepo,numberOfTopicsPerRepo)
    response =DG.sendRequest(query)
    print(DG.sendRequest(DG.queryRemainingLimit))
    
    
    org = ODH.Organization(response)
    
    graphObject =  Visualization.Graph(org)
    
    graphObject.drawInteractive()
