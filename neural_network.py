#import in_out as data
import numpy as np 
import tensorflow as tf
import random
import pandas as pd
import sklearn
from sklearn import preprocessing
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn import model_selection
from sklearn import metrics
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.metrics import accuracy_score, classification_report, auc
from sklearn.metrics import average_precision_score, plot_precision_recall_curve, precision_recall_curve
import matplotlib.pyplot as plt

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

dataset = pd.read_csv("data.csv",header=None)
dataset = dataset.sample(frac=1)
dataset_x = dataset.iloc[:,1:69].values
dataset_y = dataset.iloc[:,0].values

sc = preprocessing.StandardScaler()
X = sc.fit_transform(dataset_x)

ohe = preprocessing.OneHotEncoder()
dataset_y = np.array(dataset_y).reshape(-1,1)
Y = ohe.fit_transform(dataset_y).toarray()
#print(Y)

X_train,X_test,Y_train,Y_test = model_selection.train_test_split(X,Y,test_size = 0.2)

model = Sequential()
model.add(Dense(2500, input_dim = 68, activation='relu'))
model.add(Dense(2250, activation='relu'))
model.add(Dense(2000, activation='relu'))
model.add(Dense(1750, activation='relu')) 
model.add(Dense(1500, activation='relu'))
model.add(Dense(1250, activation='relu')) 
model.add(Dense(1000, activation='relu')) 
model.add(Dense(750, activation='relu'))
model.add(Dense(500, activation='relu')) 
model.add(Dense(250, activation='relu'))
model.add(Dense(100, activation='relu')) 
model.add(Dense(75, activation='relu'))
model.add(Dense(50, activation='relu')) 
model.add(Dense(31, activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics = ['accuracy'])

history = model.fit(X_train,Y_train,validation_split=0.1,epochs=2,batch_size=270) #270

y_pred = model.predict(X_test)
pred = list()
for i in range(len(y_pred)):
    pred.append(np.argmax(y_pred[i]))
test = list()
for i in range(len(Y_test)):
    test.append(np.argmax(Y_test[i]))

a = metrics.accuracy_score(pred,test)
print('Accuracy is:',a*100)

'''
labels = ['Normal','Memory Stress lvl 1','Memory Stress lvl 2','Memory Stress lvl 3',\
    'Disk Stress lvl 1','Disk Stress lvl 2','Disk Stress lvl 3','IO Stress lvl 1','IO Stress lvl 2','IO Stress lvl 3',\
        'CPU Stress lvl 1','CPU Stress lvl 2','CPU Stress lvl 3','Packet Loss lvl 1','Packet Loss lvl 2','Packet Loss lvl 3',\
            'Packet Duplicate lvl 1','Packet Duplicate lvl 2','Packet Duplicate lvl 3','Packet Corrupt lvl 1','Packet Corrupt lvl 2','Packet Corrupt lvl 3',\
                'Packet Reordering lvl 1','Packet Reordering lvl 2','Packet Reordering lvl 3','Bandwith Limit lvl 1','Bandwith Limit lvl 2','Bandwith Limit lvl 3',]
'''
labels1 = []
for i in range(31):
    labels1.append(i)
'''
percision = round(average_precision_score(test,pred, average='micro'),3)
recall = round(recall_score(test,pred, average = 'micro'),3)
print("Precision:" ,percision)
print("Recall:",recall)
'''

yhat = history.predict_proba(X_test)
pos_probs = yhat[:,1]

precis, recall, _ = precision_recall_curve(Y_test,pos_probs)
auc_score = auc(recall, precis)
print(auc_score)

results = confusion_matrix(test, pred)  

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(results)
plt.title('Confusion Matrix')
fig.colorbar(cax)
ax.tick_params(top = False, bottom = True, labeltop = False, labelbottom = True)
ax.set_xticks(np.arange(len(labels1)))
ax.set_yticks(np.arange(len(labels1)))
ax.set_xticklabels(labels1)
ax.set_yticklabels(labels1)

props = dict(boxstyle='round',alpha=0.5)

#plt.figtext(0.2,.3, "Percision: "+ str(percision) +"\nRecall: "+ str(recall),fontsize = 12, horizontalalignment = "center", verticalalignment = 'center')

plt.setp(ax.get_xticklabels(),rotation = 45, ha = "right", rotation_mode = "anchor")

plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

#avg_perc = average_precision_score(test,pred)
#print("Average Percision-Recall Score: ",avg_perc)


plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Model Accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Training","Testing"],loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Model Loss")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend(["Training","Testing"],loc='upper left')
plt.show()