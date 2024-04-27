# importing libraries
import pandas as pd
import numpy as np
from util import colored, normalise0to100,calcDistance
from sklearn.model_selection import train_test_split
from tkinter import *
import easygui

# load data 
#file_name = easygui.fileopenbox("Please choose the desired excel file")

OriginData = pd.read_csv("diabetes_prediction_dataset.csv") #pd.read_csv(file_name)
OriginData.dropna()
print("TEST")
print(OriginData[OriginData.columns[-1]].unique())
# Get sample size and training to test distribution
sample_size = 1 #float(easygui.enterbox("Enter Size of the sample data as fraction: "))
data = OriginData.sample(frac=sample_size).sort_index()
test_size = 0.25 #float(easygui.enterbox("Enter Size of the test data as fraction: "))
trainData, testData = train_test_split(OriginData, test_size=test_size)

# To implement naive bayes, We iterate over each test tuple.
outputClassesList = OriginData[OriginData.columns[-1]].unique()
for index,testTuple in testData.iterrows():
    outputClassesScore = []

    print(testTuple)
    # And calculate the probability of it belonging to each possible output class
    for outputClass in outputClassesList:
        classifiedTrainData = trainData[trainData.iloc[:,-1:] == outputClass]
        score = len(classifiedTrainData ) / len(trainData)
        
        # We do that by multiplying P(X|Ci) with each attribute probability
        for column_name in trainData.columns.values:

            # If it is continuous we get mean and standard deviation to calculate probability 
            attributeUniques = classifiedTrainData[column_name].unique()
            if len(attributeUniques)>10:
                x = 0
            # If the attribute is discrete we compute score 
            else: 
                matchedTuplesLen = len(classifiedTrainData[classifiedTrainData[column_name] == testTuple[column_name]])
                if matchedTuplesLen == 0:
                    score *= ( 1 / (len(classifiedTrainData) + len(classifiedTrainData[column_name].unique())) )
                else:
                    score*= (matchedTuplesLen / len(classifiedTrainData))

        outputClassesScore.append({outputClass:score})
        print(str(outputClass) + " : " + str(score))

    # After adding all the outputclasses score in the list we find the biggest one
    minNum = -1
    predictedOutputClass = ''
    for outputDic in outputClassesScore:
        for key, val in outputDic.items():
            if val > minNum:
                minNum = val
                predictedOutputClass = key
    
    print( "The Predicted Class is: " + str(predictedOutputClass))