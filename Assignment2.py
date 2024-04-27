# importing libraries
import pandas as pd
import numpy as np
from util import colored, normalise0to100,calcDistance
from tkinter import *
import easygui

# load data 
file_name = easygui.fileopenbox("Please choose the desired excel file")
OriginData = pd.read_csv(file_name)#pd.read_csv("Facebook_Live.csv")
OriginData.drop(['status_published'], axis = 1, inplace=True) 
OriginData.dropna()
# Get sample size, min support and confidence from use
sample_size = float(easygui.enterbox("Enter sample_size as fraction: "))#float(input("Enter sample_size as fraction: "))
clusterCount = int(easygui.enterbox("Enter number of clusters: "))#int(input("Enter number of clusters: "))

# We take 1 sample from each group in case sample size is too small for small groups
# Then add an equally distributed sample from each class and remove duplicates
data = pd.DataFrame(columns=OriginData.columns)
data = pd.concat([data,OriginData[OriginData["status_type"]=="link"].sample(1).sort_index()],ignore_index=True)
data = pd.concat([data,OriginData[OriginData["status_type"]=="photo"].sample(1).sort_index()],ignore_index=True)
data = pd.concat([data,OriginData[OriginData["status_type"]=="video"].sample(1).sort_index()],ignore_index=True)
data = pd.concat([data,OriginData[OriginData["status_type"]=="status"].sample(1).sort_index()],ignore_index=True)
data = pd.concat([data,OriginData[OriginData["status_type"]=="link"].sample(frac=sample_size/4).sort_index()],ignore_index=True)
data = pd.concat([data,OriginData[OriginData["status_type"]=="photo"].sample(frac=sample_size/4).sort_index()],ignore_index=True)
data = pd.concat([data,OriginData[OriginData["status_type"]=="video"].sample(frac=sample_size/4).sort_index()],ignore_index=True)
data = pd.concat([data,OriginData[OriginData["status_type"]=="status"].sample(frac=sample_size/4).sort_index()],ignore_index=True)
data = data.drop_duplicates()
# print(data)

# normalize the numerical data by setting them to range 0 to 100 as we assume they are all equals
for column_name in data.columns.values:
    max = data[column_name].max()
    min = data[column_name].min()
    # print("COL",data[column_name])
    if(column_name=="status_id" or column_name=="status_type"):
        continue
    for index, row in data.iterrows():
        # print("ROW", row)
        data.loc[data["status_id"]==row["status_id"], column_name]= normalise0to100(row[column_name],min,max)
#print(data)

# Take random K points as the centroids
centroids = data.sample(clusterCount)
tmp = []
for i in range(clusterCount):
    tmp.append([])
# with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.precision', 3):
    # print(colored(255, 0, 0,"Initial Centroid"))
    # print(colored(255, 0, 0,centroids))

for i in range(25):
    # We execute the algorithm by looping on each point, comparing it to all of the centroids and adding it to 
    # the closest one to form clusters
    for index, row in data.iterrows():
        distances = []
        for indexC, centroid in centroids.iterrows():
            distance = calcDistance(point=row, centroid=centroid)
            distances.append({"index":indexC,"distance":distance})

        # empty members list every iteration
        centroids['members'] = tmp
        min_val = float('inf')
        centroidIndex = ""
        for dic in distances:
            if dic["distance"] < min_val:
                min_val = dic["distance"]
                centroidIndex = dic["index"]
        centroids.loc[centroidIndex]['members'].append(row["status_id"])


    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.precision', 3):
        print(colored(150, 150, 0,"Intermediate centroids"))
        print(colored(150, 150, 0,centroids))
    # update centroid value depending on members
    for index, centroid in centroids.iterrows():

        # define a temp row to hold a centroid's members data sum
        count = len(centroid["members"])
        if(count==0):
            continue

        columnsNames = pd.DataFrame(columns=centroids.columns)
        updatedVals = {}
        for column_name in columnsNames.columns.values:
            updatedVals[column_name] = 0

        members = data.loc[data['status_id'].isin(centroid["members"])]
        for indexmem, member in members.iterrows():
            for column_name in members.columns.values:
                if(column_name!="status_id" and column_name!="status_type" and column_name != "members"):
                    updatedVals[column_name] += member[column_name]

        for column_name in centroids.columns.values:
            if(column_name!="status_id" and column_name!="status_type" and column_name != "members"):
                centroids.loc[index,column_name] = updatedVals[column_name]/count

message = ""
for centroid in centroids.iterrows():
    message += "\n" + str(centroid)
easygui.msgbox(title="Results",msg="Final Centroids: \n"+ message)
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.precision', 3):
    print(colored(0, 255, 0,"Final Centroid"))
    print(colored(0, 255, 0,centroids))
