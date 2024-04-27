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

# Get sample size and training to test distribution
sample_size = 1 #float(easygui.enterbox("Enter Size of the sample data as fraction: "))
data = OriginData.sample(frac=sample_size).sort_index()
test_size = 0.25 #float(easygui.enterbox("Enter Size of the test data as fraction: "))
trainData, testData = train_test_split(OriginData, test_size=test_size)

print(trainData['smoking_history'].unique())