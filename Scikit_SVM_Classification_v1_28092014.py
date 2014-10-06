#!/usr/bin/env python
# encoding: utf-8

from time import gmtime, strftime
from sklearn import svm
from sklearn import tree
from sklearn import ensemble
import json

import io, os

from sklearn.externals.six import StringIO

features = []
labels = []

numberOfSamples = 10000
trainingSamples = int(0.8 * numberOfSamples)
testingSamples = int(0.2 * numberOfSamples)

def Result_Evaluation (outputpath, testing_Labels, predict_Labels):
    acc_rate = [0, 0, 0]

    if os.path.isfile(outputpath):
        os.remove(outputpath)
    with io.open(outputpath, 'a', encoding='utf-8') as output_file:
        for i in xrange(0, testingSamples):
            rounded_result = int(round(predict_Labels[i]))
            if rounded_result == testing_Labels[i]:
                acc_rate[0] += 1
                result_item = str(i) + ": " + str(testing_Labels[i]) + " - " + str(predict_Labels[i]) + " - " + str(rounded_result) + " --> right\n"
                output_file.write(unicode(result_item))
            elif abs(rounded_result - testing_Labels[i])<=1:
                acc_rate[1] += 1
                result_item = str(i) + ": " + str(testing_Labels[i]) + " - " + str(predict_Labels[i]) + " - " + str(rounded_result) + " --> nearlyright\n"
                output_file.write(unicode(result_item))
            else:
                acc_rate[2] += 1
                result_item = str(i) + ": " + str(testing_Labels[i]) + " - " + str(predict_Labels[i]) + " - " + str(rounded_result) + " --> wrong\n"
                output_file.write(unicode(result_item))

        finalResult = "#AbsolutelyRight: " + str(acc_rate[0]) + " #NearlyRight: " + str(acc_rate[1]) + " #Wrong: " + str(acc_rate[2]) + '\n'
        output_file.write(unicode(finalResult))
        finalResultPercentage = "#AbsolutelyRight: " + str(acc_rate[0]*1.0/testingSamples) + " #NearlyRight: " + str(acc_rate[1]*1.0/testingSamples) + " #Wrong: " + str(acc_rate[2]*1.0/testingSamples) + '\n'     
        output_file.write(unicode(finalResultPercentage))


def Scikit_SVM_Classification(filename, evaluation_file):
    # read training and testing data
    with open(filename) as data_file:
        data = json.load(data_file)
        for item in data:
            features.append(item["histogram"])
            labels.append(item["rating"])

    # train the model using linear kernel, RBF kernel and polynomial
    # kernel respecively
    training_Features = features[0:trainingSamples]
    training_Labels  = labels[0:trainingSamples]
    kernel_Index = 2 #(kernel can be 1, 2, 3)
    if kernel_Index == 1:
        Scikit_SVM_Model = svm.SVC(kernel='linear')
    elif kernel_Index == 2:
        Scikit_SVM_Model = svm.SVC(kernel='rbf')
    elif kernel_Index == 3:
        Scikit_SVM_Model = svm.SVC(kernel='poly', degree=3)
    Scikit_SVM_Model.fit(training_Features, training_Labels)

    # testing
    testing_Features = features[trainingSamples:trainingSamples + testingSamples]
    testing_Labels = labels[trainingSamples:trainingSamples + testingSamples]

    predict_Labels = Scikit_SVM_Model.predict(testing_Features)
    accuracy = Scikit_SVM_Model.score(testing_Features, testing_Labels)
    print "SVM_Classification: "
    print accuracy

    Result_Evaluation (evaluation_file, testing_Labels, predict_Labels)

def Scikit_SVM_Regression(filename, evaluation_file):
    # read training data and testing data
    with open(filename) as data_file:
        data = json.load(data_file)
        for item in data:
            features.append(item['histogram'])
            labels.append(item['rating'])

    # fit regression model
    training_Features = features[0:trainingSamples]
    training_Labels  = labels[0:trainingSamples]
    kernel_Index = 2 #(kernel can be 1, 2, 3)
    if kernel_Index == 1:
        Scikit_SVR_Model = svm.SVR(kernel='linear', C=1e3)
    elif kernel_Index == 2:
        Scikit_SVR_Model = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
    elif kernel_Index == 3:
        Scikit_SVR_Model = svm.SVR(kernel='poly', C=1e3, degree=2)
    Scikit_SVR_Model.fit(training_Features, training_Labels)

    # testing
    testing_Features = features[trainingSamples:trainingSamples + testingSamples]
    testing_Labels = labels[trainingSamples:trainingSamples + testingSamples]
    

    predict_Labels = Scikit_SVR_Model.predict(testing_Features)

    accuracy = Scikit_SVR_Model.score(testing_Features, testing_Labels)
    print "SVMRegression_Classification: "
    print accuracy

    Result_Evaluation (evaluation_file, testing_Labels, predict_Labels)

def Scikit_DecisionTree_Classification(filename, evaluation_file):
    # read training data and testing data
    with open(filename) as data_file:
        data = json.load(data_file)
        for item in data:
            features.append(item['histogram'])
            labels.append(item['rating'])

    # fit classification model
    training_Features = features[0:trainingSamples]
    training_Labels  = labels[0:trainingSamples]
    Scikit_DecisionTree_Model = tree.DecisionTreeClassifier()
    Scikit_DecisionTree_Model.fit(training_Features, training_Labels)

    # Draw tree
    with open("data/tree.dot", 'w') as f:
        f = tree.export_graphviz(Scikit_DecisionTree_Model, out_file=f)

    # testing
    testing_Features = features[trainingSamples:trainingSamples + testingSamples]
    testing_Labels = labels[trainingSamples:trainingSamples + testingSamples]

    predict_Labels = Scikit_DecisionTree_Model.predict(testing_Features)
    accuracy = Scikit_DecisionTree_Model.score(testing_Features, testing_Labels)
    print "DecisionTree_Classification: "
    print accuracy

    Result_Evaluation (evaluation_file, testing_Labels, predict_Labels)

def Scikit_RandomForest_Classification(filename, evaluation_file):
    # read training data and testing data
    with open(filename) as data_file:
        data = json.load(data_file)
        for item in data:
            features.append(item['histogram'])
            labels.append(item['rating'])

    # fit classification model
    training_Features = features[0:trainingSamples]
    training_Labels  = labels[0:trainingSamples]
    Scikit_RandomForest_Model = ensemble.RandomForestClassifier(n_estimators=10)
    Scikit_RandomForest_Model.fit(training_Features, training_Labels)

    # testing
    testing_Features = features[trainingSamples:trainingSamples + testingSamples]
    testing_Labels = labels[trainingSamples:trainingSamples + testingSamples]

    predict_Labels = Scikit_RandomForest_Model.predict(testing_Features)
    accuracy = Scikit_RandomForest_Model.score(testing_Features, testing_Labels)
    print "RandomForest_Classification: "
    print accuracy

    Result_Evaluation (evaluation_file, testing_Labels, predict_Labels)

def main():
    inputfile = "data/output_split10000.json"
    starttime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    Scikit_SVM_Classification(inputfile, 'data/evaluation/evaluation_SVM.txt')
    Scikit_SVM_Regression(inputfile, 'data/evaluation/evaluation_SVMR.txt')
    Scikit_DecisionTree_Classification(inputfile, 'data/evaluation/evaluation_DT.txt')
    Scikit_RandomForest_Classification(inputfile, 'data/evaluation/evaluation_RF.txt')
    endtime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    print(starttime)
    print(endtime)

if __name__  == "__main__":
    main()





