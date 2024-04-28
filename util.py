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
        # EX: self.next = [{"next": nodeRef, "Val":"Currently Smoking"}]
        # EX: self.attributeToSplit = "Smoking History"
        self.next = []
        self.attributeToSplit = ""
        outputClasses = tuples[tuples.columns[-1]].unique()

        entropy = 0
        for outputClass in outputClasses:
            filteredTuples = tuples[tuples[tuples.columns[-1]] == outputClass]
            frequency = len(filteredTuples) / len(tuples)
            entropy -= frequency * math.log(frequency,2)

        self.outputEntropy = entropy

class DecisionTree:
    def __init__(self):
        self.head = None
    
    def insertAtBegin(self, tuples):
        new_node = Node(tuples)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node