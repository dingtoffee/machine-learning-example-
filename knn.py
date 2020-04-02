from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
import matplotlib.pyplot as plt


df1 = pd.read_csv("D:\\OneDrive\\Machine Learning Reference\\user_good.csv")
df2 = pd.read_csv("D:\\OneDrive\\Machine Learning Reference\\user_bad.csv")
df = pd.concat([df1,df2])

feature_cols = ['isnewuser','isnewip','isvpn','islan','percent','src_ip_c']
X = df[feature_cols]
y = df['tag']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.4)
k_range= range(1,26)
scores = []
for k in k_range: 
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    scores.append(metrics.f1_score(y_test, y_pred))
  
    targetname = ['Normal','Malicious']
    result = metrics.classification_report(y_test,y_pred,target_names=targetname)
    matrix = metrics.confusion_matrix(y_test, y_pred, labels = [0,1]) 
    print ('Currently running K:' + str(k))
    print (result)
    print (matrix) 

plt.plot(k_range, scores)
plt.xlabel('Value of K for KNN')
plt.ylabel('Testing F1-Score')
plt.show()
