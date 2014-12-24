#! /usr/bin/env python

import io, os
import random, json

numberOfData = 1125458

trainingRange = 800000
validationRange = 900000
testingRange = 1000000

inputfile = 'data/input/source/yelp_academic_dataset_review.json'


# Use this function to split data

#Build Bag of Words dictionary

outputfile5star = 'data/input/bow/5StarsSamples.json'
outputfile4star = 'data/input/bow/4StarsSamples.json'
outputfile3star = 'data/input/bow/3StarsSamples.json'
outputfile2star = 'data/input/bow/2StarsSamples.json'
outputfile1star = 'data/input/bow/1StarsSamples.json'

bow_NumberOfSample = 5000

bow_RandomSelectionList = random.sample(xrange(0, trainingRange), bow_NumberOfSample)

for i in xrange(1,6):
    if os.path.isfile('data/input' + str(i) + 'StarsSamples.json'):
        os.remove('data/input' + str(i) + 'StarsSamples.json')

with open(outputfile5star, 'a') as _5starfile, open(outputfile4star, 'a') as _4starfile, open(outputfile3star, 'a') as _3starfile, open(outputfile2star, 'a') as _2starfile, open(outputfile1star, 'a') as _1starfile:
    with open(inputfile) as inputfileobject:
        for i, line in enumerate(inputfileobject):
           if i in bow_RandomSelectionList:
               if line == '\n':
                    break
               data = json.loads(line)
               if data["text"] =="":
                   break
               if (data["stars"] == 5):
                   _5starfile.write((data["text"].encode('utf-8')))
               elif (data["stars"] == 4):
                   _4starfile.write((data["text"].encode('utf-8')))
               elif (data["stars"] == 3):
                   _3starfile.write((data["text"].encode('utf-8')))
               elif (data["stars"] == 2):
                   _2starfile.write((data["text"].encode('utf-8')))
               elif (data["stars"] == 1):
                   _1starfile.write((data["text"].encode('utf-8')))

#Training, validation, testing set selection

training_NumberOfSample = 400000
training_Outputfile = 'data/input/' + str(training_NumberOfSample) + 'trainingSamples.json'
training_RandomSelectionList = random.sample(xrange(0, trainingRange), training_NumberOfSample)

validation_NumberOfSample = 50000
validation_Outputfile = 'data/input/' + str(validation_NumberOfSample) + 'validationSamples.json'
validation_RandomSelectionList = random.sample(xrange(trainingRange, validationRange), validation_NumberOfSample)

testing_NumberOfSample = 50000
testing_Outputfile = 'data/input/' + str(testing_NumberOfSample) + 'testingSamples.json'
testing_RandomSelectionList = random.sample(xrange(validationRange, testingRange), testing_NumberOfSample)

#print(testing_RandomSelectionList)

if os.path.isfile(training_Outputfile):
    os.remove(training_Outputfile)
if os.path.isfile(validation_Outputfile):
    os.remove(validation_Outputfile)
if os.path.isfile(testing_Outputfile):
    os.remove(testing_Outputfile)

with open(training_Outputfile, 'a') as training_Outfile, open(validation_Outputfile, 'a') as validation_Outfile, open(testing_Outputfile, 'a') as testing_Outfile:
    with open(inputfile) as fileobject:
       for i, line in enumerate(fileobject):
           print(i)
           if i in training_RandomSelectionList:
               training_Outfile.write(unicode(line))
               #print("a")
           elif i in validation_RandomSelectionList:
               validation_Outfile.write(unicode(line))
               #print("b")
           elif i in testing_RandomSelectionList:
               testing_Outfile.write(unicode(line))
               #print("c")

print("Finish")
