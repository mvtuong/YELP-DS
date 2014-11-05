#!/usr/bin/env python
# encoding: utf-8


from time import gmtime, strftime
import json
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB

training_Features = []
training_Labels = []
testing_Features = []
testing_Labels = []

numberOfSamples = 1000
#the number of training and testing samples
trainingSamples = int(0.8 * numberOfSamples)
testingSamples = int(0.2 * numberOfSamples)

def Data_Preparation(filename):

    global training_Features
    global training_Labels
    global testing_Features
    global testing_Labels

    features = []
    labels = []
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
        accu = clf.score(testing_Features, testing_Labels)
        print("Prediction rate is: " + str(accu) + '\n')

    endtime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    print(starttime)
    print(endtime)

if __name__  == "__main__":
    main()




