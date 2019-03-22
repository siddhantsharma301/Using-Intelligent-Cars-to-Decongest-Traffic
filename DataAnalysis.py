'''
IMPORTS
'''
import itertools
import random as rand
import math
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
import copy

'''
DATA ANALYSIS
'''
class Data_Analysis:
    def __init__(self, dataset_1, dataset_2, dataset_3):
        self.dataset_1 = dataset_1
        self.dataset_2 = dataset_2
        self.dataset_3 = dataset_3
        
    def graph_dataset_1(self):
        x, y = zip(*self.dataset_1)
        plt.plot(x, y)
        plt.xlabel("Simulation iteration")
        plt.ylabel("Average System Speed (mi / h)")
        plt.title("Traffic Simulation w/o ISDs")
        plt.show()
        
    def graph_dataset_2(self):
        x, y = zip(*self.dataset_2)
        plt.plot(x, y)
        plt.xlabel("Simulation iteration")
        plt.ylabel("Average System Speed (mi / h)")
        plt.title("Traffic Simulation w/ ISDs")
        plt.show()
        
    def graph_compare_datasets(self):
        x, y1 = zip(*self.dataset_1)
        x, y2 = zip(*self.dataset_2)
        x, y3 = zip(*self.dataset_3)
        plt.plot(x, y1)
        plt.plot(x, y2)
        plt.plot(x, y3)
        plt.xlabel("Simulation iteration")
        plt.ylabel("Average System Speed (mi / h)")
        plt.title("Traffic Simulation Average Speed Comparison")
        plt.legend(['W/O ISDs', 'W/ ISDs when slow', 'W/ ISDs randomly'], loc='lower left')
        plt.show()
    
    def compare_datasets_avg(self):
        avg_dataset_1 = 0
        for i in range(len(self.dataset_1)):
            avg_dataset_1 += self.dataset_1[i][1]
        avg_dataset_1 /= len(self.dataset_1)
        
        avg_dataset_2 = 0
        for i in range(len(self.dataset_2)):
            avg_dataset_2 += self.dataset_2[i][1]
        avg_dataset_2 /= len(self.dataset_2)
        
        avg_dataset_3 = 0
        for i in range(len(self.dataset_3)):
            avg_dataset_3 += self.dataset_3[i][1]
        avg_dataset_3 /= len(self.dataset_3)
        
        print(f"No ISD vs. ISD when slow: " + str(avg_dataset_2 - avg_dataset_1))
        print(f"No ISD vs. ISD randomly: " + str(avg_dataset_3 - avg_dataset_1))
