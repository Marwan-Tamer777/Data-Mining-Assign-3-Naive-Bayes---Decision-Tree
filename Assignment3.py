# importing libraries
import pandas as pd
import numpy as np
import math
from util import colored,Node,DecisionTree
from sklearn.model_selection import train_test_split
import easygui

# load data 
#file_name = easygui.fileopenbox("Please choose the desired excel file")

OriginData = pd.read_csv("diabetes_prediction_dataset.csv") #pd.read_csv(file_name)
OriginData.dropna()
outputMessage= ""

# Get sample size and training to test distribution
sample_size = 0.01 #float(easygui.enterbox("Enter Size of the sample data as fraction: "))
data = OriginData.sample(frac=sample_size).sort_index()
test_size = 0.25 #float(easygui.enterbox("Enter Size of the test data as fraction: "))
trainData, testData = train_test_split(data, test_size=test_size)

#
#
#   Decision Tree
#
#
DC = DecisionTree()
DC.insertAtBegin(Node(trainData))
DC.buildTree(DC.head)
#DC.printTree(DC.head)

correctPreds = 0
falsePreds = 0
for index,testTuple in testData.iterrows():
    print(colored(255,0,0, str(correctPreds) + " : " + str(falsePreds)))
    predictedOutputClass = DC.predictClass(testTuple)
    if predictedOutputClass != testTuple.iloc[-1]:
        falsePreds+=1
    else:
        correctPreds+=1

print(colored(0,255,0,"Success Ratio for DC is: " + str(correctPreds/(correctPreds+falsePreds))))
outputMessage+= "DC Accuracy is: " + str(correctPreds/(correctPreds+falsePreds))
#
#
#   Naive Bayes
#
#
# To implement naive bayes, We iterate over each test tuple.
outputClassesList = OriginData[OriginData.columns[-1]].unique()
print(len(trainData))
correctPreds = 0
falsePreds = 0
for index,testTuple in testData.iterrows():
    outputClassesScore = []

    # print(testTuple)
    # And calculate the probability of it belonging to each possible output class
    for outputClass in outputClassesList:
        classifiedTrainData = trainData[trainData[trainData.columns[-1]] == outputClass]
        classifiedTrainData = classifiedTrainData.drop(classifiedTrainData.columns[-1], axis = 1)
        score = len(classifiedTrainData ) / len(trainData)
        # We do that by multiplying P(X|Ci) with each attribute probability
        for column_name in classifiedTrainData.columns.values:

            # If it is continuous we get mean and standard deviation to calculate probability 
            attributeUniques = classifiedTrainData[column_name].unique()

            if len(attributeUniques)>10:
                mean = classifiedTrainData[column_name].mean()
                std = classifiedTrainData[column_name].std()
                probablity = (math.e ** (-(testTuple[column_name]- mean)**2/2*std**2) ) / (math.sqrt(2*math.pi) * std )
                if probablity != 0:
                    score *= probablity
            # If the attribute is discrete we compute score 
            else: 
                matchedTuplesLen = len(classifiedTrainData[classifiedTrainData[column_name] == testTuple[column_name]])
                if matchedTuplesLen == 0:
                    score *= ( 1 / (len(classifiedTrainData) + len(classifiedTrainData[column_name].unique())) )
                else:
                    score*= (matchedTuplesLen / len(classifiedTrainData))

        outputClassesScore.append({outputClass:score})
        print(colored(0,0,255,str(outputClass) + " : " + str(score)))

    # After adding all the output classes score in the list we find the biggest one
    minNum = -1
    predictedOutputClass = ''
    for outputDic in outputClassesScore:
        for key, val in outputDic.items():
            if val > minNum:
                minNum = val
                predictedOutputClass = key
    
    print(colored(255,0,0,"The Predicted Class is: " + str(predictedOutputClass)))
    if predictedOutputClass != testTuple.iloc[-1]:
        falsePreds+=1
    else:
        correctPreds+=1

print(colored(0,255,0,"Success Ratio for Naive Bayes is: " + str(correctPreds/(correctPreds+falsePreds))))
outputMessage+= "Naive Bayes Accuracy is: " + str(correctPreds/(correctPreds+falsePreds))
easygui.msgbox(title="Results",msg=outputMessage)