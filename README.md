# GithubApiPlayground

I wanted to build a tool to explore how companies are organized on github. 

This in the sense of how members of that company participate in the different projects/ repositories that the company is owner for. So for user A, what projects does he participate in and how does that compare to the other in the company. The grouping of the repositories and members should also take into consideration the different topics the projects are tagged as, grouping similar together. 

The end result is a graph of a subsection of all the members in the company where red nodes represent users and blue nodes are repositories. The edge between them means that the user participates in that repository. Some repositories have edges to other repositories to represent topics they share. 

DataGatherer collects data from github. 

Organizations serve as a data structure to store the information.

Visualization handles the interactive plotting, try hovering over a node. 



To get it working set the authorization token on line 10 in "DataGatherer" to your own or send me an email and ask for mine.   

Change companies, number of repositories , numbers of users, number of topics in the main file. Sadly the Graph library gives up when you reach high numbers of nodes. 
