'''
IMPORTS
'''
import itertools
import random as rand
import math
import matplotlib.pyplot as plt
import numpy as np
import copy

'''
CAR CLASS
'''
class Car:
    id_generator = itertools.count(1)
    
    def __init__(self, car_type):
        self.car_type     = car_type
        self.id           = self.car_type + "_" + str(next(self.id_generator))
        self.x            = -5
        self.speed_lim    = 6
        
    def set_speed(self, speed):
        self.speed        = speed
        
    def incr_speed(self):
        if self.speed < self.speed_lim:
            self.speed += 1
            
    def decr_speed(self):
        if self.speed > 0:
            self.speed -= 1
            
    def brake(self):
        self.speed = math.floor(self.speed / 2)
        
    def drive(self):
        self.x = math.floor(self.x + self.speed)
'''
SUBCLASSES OF CAR
'''
class Truck(Car):
    def __init__(self):
        super().__init__('truck')
        self.speed_lim = 5

class Sedan(Car):
    def __init__(self):
        super().__init__('sedan')

class SUV(Car):
    def __init__(self):
        super().__init__('suv')
        
class Sport(Car):
    def __init__(self):
        super().__init__('sport')
        self.speed_lim = 7
