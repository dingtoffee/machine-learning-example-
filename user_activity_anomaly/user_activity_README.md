# Windows User Anomaly Detection

SOC analysts are often the first responder to cyber threats. The day to day job of a soc analyst is to hunt the malicious events from thousands of legit events. However, most of us, like myself, are often struggling with “what” we should start with once after we have used up all the traditional approaches like MITRE mapping. In this article, I will go through a use case of how we could enable anomaly detection of user login activities via machine learning which might provide a baseline/reference for other analysts.

## What are the problems that we want to solve?
User anomaly refer to the exercise of finding rare login pattern. For example, Google/Facebook will prompt you for extra authentication if they see your attempts are coming from an unseen IP address. From my day to day experience, you will know that each device has a steady pattern of login as most of the IT operations are repetitive and so their login pattern is quite straight forward. However, what will happen if your device got compromised? I assume that — In events, your device got compromised with full controls by hackers, the first step they will need to perform is to gather information about your IT environment, so most likely we will see unusual login to different devices that a normal user will not trigger — And this is what we want to validate via machine learning.
We will extract a list of login events from Windows EventViewer. 

## Lab Setup 

This is a rather basic setup with an Active Directory in place. All the servers and laptops could communicate with each other. The Active Directory is also generated with different username and password using simulation tools. A script is also created to generate daily login from different servers/laptops. I also take reference with some real live data just in case to emulate real-life situations.
Next, to perform some known bad behavior, I performed two attacks:
- lateral movement using pass-the-ticket
- User and Device enumeration using Bloodhound
All these twos are some common reconnaissance and lateral movement techniques. This forms the basics of our “normal” and “malicious” data.

## Model Selection — K- Nearest neighbors
With the sample raw log generated, I transform the evtx events into csv via one of my favorite tool from Eric Zimmerman — EvtxECmd
We will need to pick the right algorithm to start our work. Before I wrote this article, I tried to use a few different algorithms and features generation approach. In the end, I picked K-Nearest neighbors.

### K- Nearest Neighbors is: 
- Supervised machine learning algorithm as we will need to know the target variable.
- Do not make any assumption on the data distribution pattern
- Uses feature similarity to predict the cluster and where the new point will fall into.

The best thing about KNN is — they help you choose the right neighborhood to decide where the new data point belongs to. In our events, every IT environment will be different, so making the decision based on feature similarity seems ideal for us.

## Feature Generation

Feature Generation is also another problem we need to tackle. To make all our logs into meaningful events for machine learning to learn. We will need to transform our log into Machine Learning Features and dataset. I have tried a few different features including the time of login, the variance of the login.
At the end, I generated the features below:
- islan — Check whether the Source IP address is a LAN IP address (if it is a LAN IP address, it will be marked as 1. For other IP address, it will be marked as 0.)
- isnewip — Check whether the Source IP address is a new IP address accessing the server or workstation (i.e. did we see any similar login attempt from this IP address in the past 7 days?)
- isvpn — Check whether the Source IP address is a VPN IP address(if it is a VPN IP address, it will be marked as 1. For other IP address, it will be marked as 0.)
- percent — The total number of Login Event coming from this IP address/ total number of Login event for that server (past 1 day)
- src_ip_c — The count of successful Login in 15 minutes sliding windows.
- tag — 1 stands for malicious traffic and 0 stands for normal traffic.

## Results
As a result, I plotted a graph with various number of K against the F1-score of the model.
K=4 performs the best. 

Link to [my article](https://medium.com/analytics-vidhya/cyber-security-in-machine-learning-windows-user-anomaly-detection-e0d3457dea32).

