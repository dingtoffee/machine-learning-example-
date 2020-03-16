import pandas as pd # import pandas function 
from sklearn.metrics import classification_report # import classification result 
from sklearn.tree import DecisionTreeClassifier # import decision tree model 
from sklearn.model_selection import train_test_split # Import train_test_split function

# read the data 
data  = pd.read_csv("D:\\OneDrive\\Machine Learning Reference\\firewall_traffic_20200316.csv", header = 0)
# features used for evaluation 
feature_cols = ['TOTAL', 'accept_count', 'date_occurance', 'deny_count', 'internet', 'ip_c', 'isinfra', 'protco_count']
X = data[feature_cols]
# Y axis i.e. the column that prediction is going to run 
y = data.tag
# split the csv file into testing and training 
X_train, X_test, y_train, y_test =train_test_split(X, y, test_size=0.4, random_state=1)

clf = DecisionTreeClassifier(criterion='entropy')
clf = clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)

target_names = ['Normal','IPSWEEP','Port Scan']

result = classification_report(y_test, y_predict, target_names = target_names)

print (result) 
