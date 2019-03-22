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
import copy
from Car import Car, Truck, Sedan, SUV, Sport

"""
#############################################################################################################################################################################################################################################
SIMULATION MECHANISM
#############################################################################################################################################################################################################################################
"""
class Sim:
    """
    This class represents a traffic Simulation object
    Uses Car objects to represent cars
    """
    def __init__(self):
        self.CAR_LENGTH      = 6      
        self.road_length     = self.CAR_LENGTH * 20 
        self.desired_speed   = 7     
        self.ideal_time      = self.road_length / self.desired_speed      
        
        self.iteration       = 0
        self.cars            = []
        self.init_cars()
        self.avg_speed       = {}
        
        
    def init_cars(self):
        self.cars.append(self.generate_car())

        
    def generate_car(self):
        speed = 6     
        car_chooser = rand.randint(0,3)
        if car_chooser == 0:
            car = Truck()
        elif car_chooser == 1:
            car = SUV()
        elif car_chooser == 2:
            car = Sport()
        else:
            car = Sedan()
            
        car.set_speed(speed)
        return car
    
    
    def step(self):
        if self.cars[0].x > self.road_length:
            self.cars.pop(0)
        
        fender_distance = None
        cars_total_speed = self.cars[0].speed

        if self.CAR_LENGTH * 1.25 < self.cars[-1].x:
            self.cars.append(self.generate_car())

        self.cars[0].drive()
        self.cars[0].incr_speed()
        
        for i in range(len(self.cars)):
            self.cars[i].drive()

            if len(self.cars) != 1 & i != 0:
                fender_dist = self.cars[i - 1].x - self.cars[i].x
                
                self.cars[i].incr_speed()    if fender_dist > self.CAR_LENGTH * 1.25      else None
                self.cars[i].decr_speed()    if fender_dist < self.CAR_LENGTH * 1.25      else None
                self.cars[i].brake()         if fender_dist < self.CAR_LENGTH * 0.625    else None

                cars_total_speed += self.cars[i].speed

                
        self.cars = self.cars[-20:]
        self.avg_speed[self.iteration] = cars_total_speed / len(self.cars)
            
        self.iteration += 1
            
            
    def data_analysis(self):
        self.avg_speed = sorted(self.avg_speed.items())
        x, y = zip(*self.avg_speed)
        plt.plot(x, y)
        plt.xlabel("Simulation iteration")
        plt.ylabel("Average System Speed (mi / h)")
        plt.title("Traffic Simulation w/o ISDs")
        plt.show()
