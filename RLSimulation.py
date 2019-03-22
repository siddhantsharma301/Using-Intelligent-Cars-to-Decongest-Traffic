'''
IMPORTS
'''
import itertools
import random as rand
import math
import matplotlib.pyplot as plt
import numpy as np
import copy
from Car import Car, Truck, Sedan, SUV, Sport
from ISD import ISD

'''
SIMULATION MECHANISM
'''
class Simulation:
    CAR_LENGTH           = 6
    ROAD_LENGTH          = CAR_LENGTH * 20
    DESIRED_SPEED        = 6
    
    def __init__(self):
        self.cars        = []
        self.init_cars()
        self.iteration   = 0
        self.avg_speed   = {}
        
    def init_cars(self):
        self.cars.append(self.generate_car())
        
    def generate_car(self):
        speed = 6
        n = rand.randint(0, 3)
        if n == 0:
            car = Truck()
        elif n == 1:
            car = Sedan()
        elif n == 2:
            car = SUV()
        else:
            car = Sport()
        car.set_speed(speed)
        return car
    
    def step(self):
        if self.cars[0].x > self.ROAD_LENGTH:
            self.cars.pop(0)
        
        fender_dist = None
        total_speed = self.cars[0].speed
        
        if self.CAR_LENGTH * 1.25 < self.cars[-1].x:
            self.cars.append(self.generate_car())
            
        self.cars[0].drive()
        self.cars[0].incr_speed()
        
        for i in range(len(self.cars)):
            self.cars[i].drive()
            
            if i != 0:
                fender_dist = self.cars[i - 1].x - self.cars[i].x
                
                self.cars[i].incr_speed()    if fender_dist > self.CAR_LENGTH * 1.25      else None
                self.cars[i].decr_speed()    if fender_dist < self.CAR_LENGTH * 1.25      else None
                self.cars[i].brake()         if fender_dist < self.CAR_LENGTH * 0.625     else None

                total_speed += self.cars[i].speed
                
        self.avg_speed[self.iteration] = total_speed / len(self.cars)
        self.iteration += 1
        
    def data_analysis(self):
        self.avg_speed = sorted(self.avg_speed.items())
        x, y = zip(*self.avg_speed)
        plt.plot(x, y)
        plt.xlabel("Simulation iteration")
        plt.ylabel("Average System Speed (mi / h)")
        plt.title("Traffic Simulation w/o ISDs")
        plt.show()

'''
REINFORCED LEARNING TRAINED SIMULATION
'''
class RLSimulation(Simulation):
    def __init__(self, alpha, gamma):
        super().__init__()
        
        self.alpha              = alpha
        self.gamma              = gamma
        
        self.n_actions          = 4
        self.n_sys_speed        = 8
        self.n_isd_speed        = 7
        self.n_car_type         = 4
        self.n_car_speed        = 8
        self.Qmat               = [[[[{0: 0., 1: 0., 2: 0. , 3: 0.}
                                     for _ in range(self.n_car_speed)]
                                    for _ in range(self.n_car_type)]
                                   for _ in range(self.n_isd_speed)]
                                  for _ in range(self.n_sys_speed)]
        
        self.speed_incr_reward =  50
        self.speed_same_reward =  10
        self.speed_decr_reward = -20
        self.default_reward    = -1
        
        self.isd_present       = False
        self.isd               = self.generate_isd()
        self.isd.set_state(None, None, None, None)
        
        self.curr_speed        = 0
        
    def generate_isd(self):
        car = ISD()
        car.set_speed(6)
        return car
    
    def setup_training(self):
        self.train_isd         = self.generate_isd()
        self.train_isd.set_state(None, None, None, None)
        self.train_isd_present = False
        self.train_isd_index   = -1
        self.train_cars        = []
        self.train_iteration   = 0
        self.train_avg_speed   = {}
        self.train_cars.append(self.generate_car())
        self.train_car_behind  = False
        
    def train(self, e = 0.1):
        self.train_pop()
                
        fender_dist = None
        total_speed = self.train_cars[0].speed
        
        self.train_add_car()
           
        if self.train_car_behind:
            action = self.train_each_action(e) 
        
        for i in range(len(self.train_cars)):
            self.train_cars[i].drive()
            
            if i != 0:
                fender_dist = self.train_cars[i - 1].x - self.train_cars[i].x
                if self.train_cars[i].car_type != 'isd' or self.train_car_behind == False:
                    self.train_cars[i].incr_speed()    if fender_dist > self.CAR_LENGTH * 1.25      else None
                    self.train_cars[i].decr_speed()    if fender_dist < self.CAR_LENGTH * 1.25      else None
                    self.train_cars[i].brake()         if fender_dist < self.CAR_LENGTH * 0.625     else None
                else:
                    if action == 0:
                        self.train_cars[i].incr_speed()
                    elif action == 1:
                        self.train_cars[i].decr_speed()
                    elif action == 2:
                        self.train_cars[i].brake() 
                    else:
                        None
                    
                total_speed += self.train_cars[i].speed
            
        self.train_avg_speed[self.train_iteration] = total_speed / len(self.train_cars)
        self.curr_speed = int(self.train_avg_speed[self.train_iteration])
        self.train_iteration += 1
           
    def train_pop(self):
         if self.train_cars[0].x > self.ROAD_LENGTH:
            if self.train_cars[0].car_type == 'isd':
                self.train_isd_present = False
                self.train_isd_index   = -1
                self.train_car_behind  = False
                self.train_isd = self.generate_isd()
                self.train_isd.set_state(None, None, None, None)
            
            self.train_cars.pop(0)
            
            if self.train_isd_present == True:
                self.train_isd_index -= 1
                
    def train_add_car(self):
        if self.CAR_LENGTH * 1.25 < self.train_cars[-1].x:
            if self.train_iteration > 0 and self.curr_speed  < 6 and self.train_isd_present == False:
                self.train_cars.append(self.train_isd)
                self.train_isd_present = True
                self.train_isd_index   = len(self.train_cars) - 1
                
            else: 
                self.train_cars.append(self.generate_car())
                if self.train_isd_present:
                    car_behind = self.train_cars[self.train_isd_index + 1]
                    car_type   = self.type_to_num(car_behind.car_type)
                    car_speed  = car_behind.speed
                    self.train_isd.set_state(self.curr_speed, self.train_isd.speed, car_type, car_speed)
                    self.train_car_behind = True
                    
    def train_each_action(self, e):
        [curr_sys_speed, curr_speed, curr_car_type, curr_car_speed] = self.train_isd.state
        car_type = self.type_to_num(curr_car_type)
        for i in range(self.n_actions):
            train_copy = copy.deepcopy(self.train_isd)
            train_cars_copy = self.train_cars.copy()
            outcome = self.train_next_step(train_copy, self.train_isd_index, train_cars_copy, i)
            reward = self.check_reward(curr_sys_speed, outcome[0])
            action = train_copy.select_e_greedily(self.Qmat, e = e)
            
            self.Qmat[curr_sys_speed - 1][curr_speed - 1][car_type][curr_car_speed - 1][i] += self.alpha *                (reward + self.gamma * self.Qmat[int(outcome[0]) - 1][outcome[1] - 1][car_type][outcome[2] - 1][action] -
                 self.Qmat[curr_sys_speed - 1][curr_speed - 1][car_type][curr_car_speed - 1][i])
            
    def train_next_step(self, isd, isd_index, cars, action):
        fender_dist = None
        total_speed = cars[0].speed
        
        if self.CAR_LENGTH * 1.25 < cars[-1].x:
            cars.append(self.generate_car())
            
        cars[0].drive()
        cars[0].incr_speed()
        
        for i in range(len(cars)):
            cars[i].drive()
            
            if i != 0: 
                fender_dist = cars[i - 1].x - cars[i].x
                
                if cars[i].car_type != 'isd':
                    cars[i].incr_speed()    if fender_dist > self.CAR_LENGTH * 3      else None
                    cars[i].decr_speed()    if fender_dist < self.CAR_LENGTH * 3      else None
                    cars[i].brake()         if fender_dist < self.CAR_LENGTH * 1.5    else None
                else:
                    if action == 0:
                        cars[i].incr_speed()
                    elif action == 1:
                        cars[i].decr_speed()
                    elif action == 2:
                        cars[i].brake()
                    else:
                        None
            total_speed += cars[i].speed
            
        sys_avg = total_speed / len(cars)
        isd_speed = cars[isd_index].speed
        car_speed = cars[isd_index + 1].speed
        return sys_avg, isd_speed, car_speed
    
    def check_reward(self, init_speed, curr_speed):
        if curr_speed > init_speed:
            return self.speed_incr_reward
        elif curr_speed < init_speed:
            return self.speed_decr_reward
        elif abs(curr_speed - init_speed) <= 0.0001:
            return self.speed_same_reward
        else:
            return self.default_reward
        
    def training_data_analysis(self):
        self.train_avg_speed = sorted(self.train_avg_speed.items())
        x, y = zip(*self.train_avg_speed)
        plt.plot(x, y)
        plt.xlabel("Simulation iteration")
        plt.ylabel("Average System Speed (mi / h)")
        plt.title("Traffic Simulation Training w/ ISDs")
        plt.show()
        
    def type_to_num(self, car_type):
        if car_type == 'truck':
            return 0
        elif car_type == 'sedan':
            return 1
        elif car_type == 'suv':
            return 2
        else:
            return 3
        
    def setup_step(self):
        self.isd               = self.generate_isd()
        self.isd.set_state(None, None, None, None)
        self.isd_present       = False
        self.isd_index         = -1
        self.cars              = []
        self.iteration         = 0
        self.avg_speed         = {}
        self.cars.append(self.generate_car())
        self.car_behind        = False
        self.curr_speed        = 0
        
    def step_when_slow(self):
        if self.cars[0].x > self.ROAD_LENGTH:
            if self.cars[0].car_type == 'isd':
                self.isd_present = False
                self.isd_index   = -1
                self.car_behind  = False
                self.isd = self.generate_isd()
                self.isd.set_state(None, None, None, None)
            
            self.cars.pop(0)
            
            if self.isd_present == True:
                self.isd_index -= 1
        
        fender_dist = None
        total_speed = self.cars[0].speed
        
        if self.CAR_LENGTH * 1.25 < self.cars[-1].x:
            if self.iteration > 0 and self.curr_speed  < 6 and self.isd_present == False:
                self.cars.append(self.isd)
                self.isd_present = True
                self.isd_index   = len(self.cars) - 1
                
            else: 
                self.cars.append(self.generate_car())
                if self.isd_present:
                    car_behind_isd = self.cars[self.isd_index + 1]
                    car_type   = self.type_to_num(car_behind_isd.car_type)
                    car_speed  = car_behind_isd.speed
                    self.isd.set_state(self.curr_speed, self.isd.speed, car_type, car_speed)
                    self.car_behind = True
            
        self.cars[0].drive()
        self.cars[0].incr_speed()
        
        if self.car_behind:
            action = self.isd.select_e_greedily(self.Qmat, e = 0.1)
            
        for i in range(len(self.cars)):
            self.cars[i].drive()
            
            if i != 0:
                fender_dist = self.cars[i - 1].x - self.cars[i].x
                
                if self.cars[i].car_type != 'isd' or self.car_behind == False:
                    self.cars[i].incr_speed()    if fender_dist > self.CAR_LENGTH * 1.25      else None
                    self.cars[i].decr_speed()    if fender_dist < self.CAR_LENGTH * 1.25      else None
                    self.cars[i].brake()         if fender_dist < self.CAR_LENGTH * 0.625     else None
                else:
                    if action == 0:
                        self.cars[i].incr_speed()
                    elif action == 1:
                        self.cars[i].decr_speed()
                    elif action == 2:
                        self.cars[i].brake()
                    else:
                        None

                total_speed += self.cars[i].speed
                
        self.avg_speed[self.iteration] = total_speed / len(self.cars)
        self.iteration += 1
        
    def step(self):
        if self.cars[0].x > self.ROAD_LENGTH:
            self.cars.pop(0)
        
        fender_dist = None
        total_speed = self.cars[0].speed
        
        if self.CAR_LENGTH * 1.25 < self.cars[-1].x:
            self.cars.append(self.step_generate_car())
            
        self.cars[0].drive()
        self.cars[0].incr_speed()
        
        for i in range(len(self.cars)):
            self.cars[i].drive()
            
            if i != 0:
                fender_dist = self.cars[i - 1].x - self.cars[i].x
                
                self.cars[i].incr_speed()    if fender_dist > self.CAR_LENGTH * 1.25      else None
                self.cars[i].decr_speed()    if fender_dist < self.CAR_LENGTH * 1.25      else None
                self.cars[i].brake()         if fender_dist < self.CAR_LENGTH * 0.625     else None

                total_speed += self.cars[i].speed
                
        self.avg_speed[self.iteration] = total_speed / len(self.cars)
        self.iteration += 1
        
    def step_generate_car(self):
        speed = 6
        n = rand.randint(0, 4)
        if n == 0:
            car = Truck()
        elif n == 1:
            car = Sedan()
        elif n == 2:
            car = SUV()
        elif n == 3:
            car = Sport()
        else:
            car = ISD()
        car.set_speed(speed)
        return car
    
    def data_analysis(self):
        self.avg_speed = sorted(self.avg_speed.items())
        x, y = zip(*self.avg_speed)
        plt.plot(x, y)
        plt.xlabel("Simulation iteration")
        plt.ylabel("Average System Speed (mi / h)")
        plt.title("Traffic Simulation w/ ISDs")
        plt.show()
