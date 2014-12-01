#!/usr/bin/env python
# encoding: utf-8


from time import gmtime, strftime
import json
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import r2_score
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB

training_Features = []
training_Labels = []
testing_Features = []
testing_Labels = []

features = []
labels = []

numberOfSamples = 1000
#the number of training and testing samples
trainingSamples = int(0.8 * numberOfSamples)
testingSamples = int(0.2 * numberOfSamples)

def Data_Preparation(filename):

    global training_Features
    global training_Labels
    global testing_Features
    global testing_Labels

    global features
    global labels 
    # read training and testing data
    with open(filename) as data_file:
        data = json.load(data_file)
        for item in data:
            features.append(item["histogram"])
            labels.append(item["rating"])

    #training
    training_Features = features[0:trainingSamples]
    training_Labels = labels[0:trainingSamples]
    # testing
    testing_Features = features[trainingSamples:trainingSamples + testingSamples]
    testing_Labels = labels[trainingSamples:trainingSamples + testingSamples]

def main():
    starttime = strftime("%Y-%m-%d %H:%M:%S",gmtime())

    inputfile = "data/output/histogram.json"

    print("Preparing data ...")
    Data_Preparation(inputfile)
    print("Finished preparing data ...\n")
  
    clfs = [GaussianNB(), MultinomialNB(), BernoulliNB()]
    for i in range(0,3):
        clf = clfs[i]
        clf.fit(training_Features, training_Labels)
        predict_Labels = clf.predict(testing_Features)
        #predict_log = clf.predict_log_proba(testing)
        #predict_proba = clf.predict_proba(testing)
        accu = clf.score(testing_Features, testing_Labels)
        print("Prediction rate is: " + str(accu) + '\n')
    
        print("Starting SVM Classification ...")
        kernel_Index = 1
        if kernel_Index == 1:
            Scikit_SVM_Model = svm.SVC(kernel='linear')
        elif kernel_Index == 2:
            Scikit_SVM_Model = svm.SVC(kernel='rbf')
        elif kernel_Index == 3:
            Scikit_SVM_Model = svm.SVC(kernel='poly', degree=3)
        print("Training ..")
    
        #the output of Naive Bayes is sent to the SVM classifier
        kf = cross_validation.KFold(numberOfSamples, n_folds=5, shuffle=False, random_state=None)
        X = np.array(features)
        y = np.array(labels)
        for train_index, test_index in kf:
            #print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = X[train_index], X[test_index]
            #print ("X_TRAIN:", X_train, "X_TEST:", X_test)
            y_train, y_test = y[train_index], y[test_index]
            #print ("y_TRAIN:", y_train, "y_TEST:", y_test)

            Scikit_SVM_Model.fit(X_train, y_train)
            print("Testing ..")
            predict_Labels = Scikit_SVM_Model.predict(X_test)
            accuracy = Scikit_SVM_Model.score(X_test, y_test)
            print "SVM_Classification: "
            print accuracy
        
            #the implementation of R_2 score measure 
            r2Score = r2_score(testing_Labels, predict_Labels)
            print("R2 Square score of SVM CrossValidation Classification: " + str(r2Score)) 
  
    endtime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    print(starttime)
    print(endtime)

if __name__  == "__main__":
    main()





