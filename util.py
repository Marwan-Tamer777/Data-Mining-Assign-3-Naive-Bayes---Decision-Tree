import pandas as pd
import numpy as np
import math

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


# For Decision Tree we create a data structure for the nodes and decision tree (very similar to linked list)
class Node:
    # Each node is initialized with its dataFrame and its entropy as a parent node is calculated
    def __init__(self, tuples):
        self.tuples = tuples
        # Next list holds all the other nodes and the attribute value they are split upon
        # EX: self.next = [{"node": nodeRef, "val":"Currently Smoking"}]
        # EX: self.attributeToSplit = "Smoking History"
        self.next = []
        self.attributeToSplit = ""
        self.leafNode = False
        self.finalClass = ""

        outputClasses = tuples[tuples.columns[-1]].unique()
        entropy = 0
        for outputClass in outputClasses:
            filteredTuples = tuples[tuples[tuples.columns[-1]] == outputClass]
            frequency = len(filteredTuples) / len(tuples)
            entropy -= frequency * math.log(frequency,2)
        self.outputEntropy = entropy
    
    def computeBestAttributeWithInfoGain(self):
        bestAttribute = ''
        attributesInformationGain = []
        outputClasses = self.tuples[self.tuples.columns[-1]].unique()

        
        # For each discrete attribute we split on its possible value and 
        # Compute each child entropy relative to that attribute so 
        # we can compute each attribute Information Gain
        for column_name in self.tuples.columns.values:
            possibleValues = self.tuples[column_name].unique()
            if column_name not in ['diabetes', 'age','bmi','HbA1c_level','blood_glucose_level']:

                entropy = 0
                for possibleValue in possibleValues:
                    childData = self.tuples[self.tuples[column_name] == possibleValue]

                    base = 0
                    for outputClass in outputClasses:
                        filteredTuples = childData[childData[childData.columns[-1]] == outputClass]
                        frequency = len(filteredTuples) / len(childData)
                        if frequency != 0:
                            base -= frequency * math.log(frequency,2)
                    entropy += base* len(childData)/ len(self.tuples)
                    
                attributesInformationGain.append({column_name:entropy})
        
        # After iterating through all attributes and getting their entropy,
        # We pick the attribute with the smallest entropy.
        maxNum = 2
        for attributeDic in attributesInformationGain:
            for key, val in attributeDic.items():
                if val < maxNum:
                    maxNum = val
                    bestAttribute = key

        return bestAttribute

    def printNode(self):
        print(" A NODE.")
        print(self.tuples)
        print(self.attributeToSplit)
        print(self.leafNode)
        print(self.finalClass)
        print()
class DecisionTree:
    def __init__(self):
        self.head = None
    
    def insertAtBegin(self, Node):
        if self.head is None:
            self.head = Node
            return
        else:
            Node.next = self.head
            self.head = Node
    
    def buildTree(self,node):
        if node is None:
            return
        
        nodeData = node.tuples
        bestAttribute = node.computeBestAttributeWithInfoGain()

        outputClasses = nodeData[nodeData.columns[-1]].unique()

        # If we try to split a node and find out all its classes are equal
        # we connect it to a leaf node to terminate 
        if len(outputClasses) == 1:
            node.leafNode = True
            node.finalClass = outputClasses[0]
            return

        # If we try to get best attribute and it returns empty
        # This should mean that we reached a leaf node yet the values aren't unanimous we cannot split further
        if bestAttribute== '':
            node.leafNode = True
            node.finalClass = node.tuples[node.tuples.columns[-1]].mode().values[0]
            return
        node.attributeToSplit = bestAttribute
        possibleValues = nodeData[bestAttribute].unique()

        # If we can split then we iterate over all values for that attribute
        # Create a new node for each then link to the parent node
        # And we drop the attribute column so it doesn't get chosen again in children nodes
        for possibleValue in possibleValues:
            tuples = nodeData[nodeData[bestAttribute]==possibleValue]
            tuples = tuples.drop(bestAttribute, axis = 1)
            new_node = Node(tuples)
            # Recursion to build all of the tree
            self.buildTree(new_node)
            node.next.append({"node": new_node, "val":possibleValue})

    def printTree(self,node):
        if node is None:
            return


        if node.leafNode ==True:
            node.printNode()
            return
        
        node.printNode()
        for child in node.next:
            print("We move to the next node through value: " + child['val'])
            self.printTree(child['node'])

    def predictClass(self,tuple):
        node = self.head

        while(node.leafNode != True):
            print(2)
            children = []
            children = node.next
            for child in children:
                # node.printNode()
                if(node.attributeToSplit == ''):
                    return node.finalClass
                if(child['val'] == tuple[node.attributeToSplit]):
                    node = child['node']
                    
        return node.finalClass