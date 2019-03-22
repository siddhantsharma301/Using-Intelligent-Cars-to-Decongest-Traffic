"""
#############################################################################################################################################################################################################################################
IMPORTS
#############################################################################################################################################################################################################################################
"""
import itertools
import random as rand
import math
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
import copy
from Car import Car

"""
#############################################################################################################################################################################################################################################
ISD CLASS
#############################################################################################################################################################################################################################################
"""
class ISD(Car):
    def __init__(self):
        super().__init__('isd')
    
    def set_state(self, sys_speed, isd_speed, car_type, car_speed):
        self.state = [sys_speed, isd_speed, car_type, car_speed]
        
    def decr_speed(self):
        if self.speed > 1:
            self.speed -= 1
    
    def brake(self):
        self.speed = math.floor(self.speed / 2) if math.floor(self.speed / 2) else 1
        
    def select_e_greedily(self, Qmat, e):
        [sys_speed, isd_speed, car_type, car_speed] = self.state
        choices = Qmat[sys_speed - 1][isd_speed - 1][car_type][car_speed - 1]
        
        if np.random.uniform(0, 1) < e:
            return np.random.choice(list(choices.keys()))
        else:
            return max(choices, key = choices.get)
