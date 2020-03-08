# -*- coding: utf-8 -*-
"""
module for building queries and communications.

input your token below
"""
import requests

#Put your own token here instead of %%
headers = {"Authorization": "token %%"}

'''
Sending requests - Based on githubs tutorial 
'''
def sendRequest(query):



    request = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        print("Query failed to run by returning code of {}. {}".format(request.status_code, query))
        return False
        
'''
Constructing the query,max number of repos, max number of members from the repos, max number of topics 
'''
def constructDatarequest(CompanyName,repoDepth,memberDepth,topicDepth):
    queryGetRepoAndMembers ="""
    {{    
    organization(login :"{}" ) 
        {{
        name
        repositories(first : {})
            {{
            nodes
                {{
                name
                mentionableUsers(first :{})
                    {{
                    totalCount 
                    nodes
                        {{
                        login
                        }} 
                    }}
                
                repositoryTopics(first:{})
                    {{
                    nodes
                        {{
                        topic
                            {{
                            name
                            }}
                        }}
                    }}
                }}
            
            }}
                    
        }}    
    
    }}
    """.format(CompanyName,repoDepth,memberDepth,topicDepth)
    
    return queryGetRepoAndMembers

# limit check query
queryRemainingLimit=""" {
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
"""



    #debug
if __name__ == "__main__":
    query = constructDatarequest("futurice",1,1,1)
    r =sendRequest(query)
    print( r)
 
    