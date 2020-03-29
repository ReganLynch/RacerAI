from game_settings import *
from car import *
import copy
import random

#gets the car to be used in the next generation
#using roulette-wheel selction
def select_car_to_live(cars):
    sum = 0
    #get the sum of all scores
    for car in cars:
        sum += car.score
    #generate a number between 0 and the sum of scores
    end_point = random.uniform(0, sum)
    #sort the list of cars based on their score,
    cars.sort(key=lambda x: x.score, reverse=True)
    #go through all cars, adding the cars score to the running score.
    #if the running score is greater than the end point, return the current car
    running_score = 0
    for car in cars:
        running_score += car.score
        if running_score >= end_point:
            return car

#this returns the next generation
def get_next_generation(cars):
    best_car = select_car_to_live(cars).copy()
    ret_cars = []
    ret_cars.append(best_car)
    for i in range(1, population_size):
        new_car = best_car.copy()
        new_car.mutate(learning_rate)
        ret_cars.append(new_car)
    return ret_cars
