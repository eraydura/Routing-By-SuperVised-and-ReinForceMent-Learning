# -*- coding: utf-8 -*-
"""
Writen by Eray Dura

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G8fh2dSHldOlQ4SqGFmLAkwULzXXTcJN
"""
from keras.layers import Dense
from keras.optimizers import Adam
from keras.metrics import MeanSquaredError
from sklearn.model_selection import KFold
from keras.models import Sequential
from keras import Model,Input
from sklearn.model_selection import train_test_split
import numpy as np
import sys
import csv

#random seed for reproducibility
seed = 7
np.random.seed(seed)

input_train = []
target_train = []

#Bellman-Ford Algorithm for shortest path
def getPath(parent, vertex):
    if vertex < 0:
        return []
    return getPath(parent, parent[vertex]) + [vertex]

def bellmanFord(edges, source, n):
    distance = [sys.maxsize] * n
    parent = [-1] * n
    distance[source] = 0

    for k in range(n - 1):
        for (u, v, w) in edges:
            if distance[u] != sys.maxsize and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                parent[v] = u

    #Negative Path
    for (u, v, w) in edges:
        if distance[u] != sys.maxsize and distance[u] + w < distance[v]:
            return

    for i in range(n):
        input = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        target = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        if i != source and distance[i] < sys.maxsize:
            input[i]=1
            input[source] = 1
            for x in getPath(parent, i):
                target[x]=1
            input_train.append(input)
            target_train.append(target)
      
paths = [
    (0, 1, 4), (0, 7, 8), (1, 7, 11), (1, 2, 8),
    (2, 8, 2), (2, 3, 7), (2, 5, 4), (7, 8, 7),
    (7, 6, 1), (8, 6, 6), (6, 5, 2), (5, 3, 14),
    (3, 4, 9), (5, 4, 10)
]

for source in range(9):
    bellmanFord(paths, source, 9)

input_train = np.repeat(np.array(input_train), 8)
target_train = np.repeat(np.array(target_train), 8)
input_train, input_test, target_train, target_test = train_test_split(input_train, target_train, test_size=0.33, random_state=1)
inputs = np.concatenate((input_train, input_test), axis=0)
targets = np.concatenate((target_train, target_test), axis=0)

# Define the K-fold Cross Validator
kfold = KFold(n_splits=5, shuffle=True , random_state=seed)

# K-fold Cross Validation model evaluation
fold_no = 1
acc_per_fold=[]
loss_per_fold=[]

def create_model(learning_rate):
  model = Sequential()

  # First hidden layer with 20 nodes.   
  model.add(Dense(units=20, activation='sigmoid', name='Hidden1'))
  
  # Second hidden layer with 12 nodes. 
  model.add(Dense(units=12, activation='sigmoid', name='Hidden2'))
  
  # Output layer.
  model.add(Dense(units=1, activation='sigmoid', name='Output'))                              
  
  #Mean Squared Error & Accuracy metric
  model.compile(optimizer=Adam(learning_rate=learning_rate),loss="mean_squared_error",metrics=['accuracy'])

  return model

def testable(fold_no,model,x_test,y_test):
  csvfile='predictedcsv'+str(fold_no)
  data_list = [["input", "target", "prediction"]]
  for i in range(len(x_test)):
    prediction=model.predict(np.asarray(x_test[i]).astype('float32').reshape(-1, 1, 9, 1))
    data_list.append([x_test[i].reshape(1,9),y_test[i].reshape(1,9),np.rint(prediction.reshape(1,9))])
  with open(csvfile, 'w', newline='') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerows(data_list)
  
for train, test in kfold.split(inputs, targets):

  x= np.asarray(inputs[train]).astype('float32').reshape(-1, 1, 9, 1)
  y= np.asarray(targets[train]).astype('float32').reshape(-1, 1, 9, 1)
  x_test= np.asarray(inputs[test]).astype('float32').reshape(-1, 1, 9, 1)
  y_test= np.asarray(targets[test]).astype('float32').reshape(-1, 1, 9, 1)

  model= create_model(0.01)

  # Generate a print
  print('------------------------------------------------------------------------')
  print(f'Training for fold {fold_no} ...')

  # Fit data to model
  history = model.fit(x, y,
              batch_size=32,
              validation_split=0.3,
              epochs=30,
              verbose=1)
  
  # Generate generalization metrics
  scores = model.evaluate(x_test, y_test, verbose=0)
  testable(fold_no,model,x_test,y_test)
  print(f'Score for fold {fold_no}: {model.metrics_names[0]} of {scores[0]}; {model.metrics_names[1]} of {scores[1]*100}%')
  acc_per_fold.append(scores[1])
  loss_per_fold.append(scores[0])
  
  # Increase fold number
  fold_no = fold_no + 1

print("Accuracy Scores: %.2f%% (+/- %.2f%%)" % (np.mean(acc_per_fold), np.std(acc_per_fold)))
print("Loss Scores: %.2f%% (+/- %.2f%%)" % (np.mean(loss_per_fold), np.std(loss_per_fold)))

