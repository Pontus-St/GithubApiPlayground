# GithubApiPlayground

**Description:**
I wanted to build a tool to explore how companies are organized on github. 

This in the sense of how members of that company participate in the different projects/ repositories that the company is owner for. So for user A, what projects does he participate in and how does that compare to the other in the company. The grouping of the repositories and members should also take into consideration the different topics the projects are tagged as, grouping similar together. 

The end result is a graph of a subsection of all the members in the company where red nodes represent users and blue nodes are repositories. The edge between them means that the user participates in that repository. Some repositories have edges to other repositories to represent topics they share. 

DataGatherer collects data from github. 

Organizations serve as a data structure to store the information.

Visualization handles the interactive plotting, try hovering over a node. 

**To get it working:**
set the authorization token on line 10 in "DataGatherer" to your own by visiting https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line.

if your have your own token check that it has the permission **read:org** which can be found under admin:org. An already created token can be altered in github >settings > developer settings> clicking the key > selecting premissions > clicking update token

libraries used can be found in the requirements.txt file and can be installed through pip. Command on windows is "python -m pip install -r requirements.txt"

to start the program run main.py, this will run an example on google's repositories.

To change company, number of repositories, number of members and topics change the values in main.py  in lines 33-35 

Below is an example of setting Futurice as the company

![alt text](https://github.com/Pontus-St/GithubApiPlayground/blob/master/userExample.png)
