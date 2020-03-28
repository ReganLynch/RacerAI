from game_settings import *
from car import *
import copy


#gets the best car of the generation
#SHOULDNT JUST GET BEST CAR -> SHOULD BE BASED ON PROBABILITY
def get_best_car(cars):
    best_car = cars[0]
    for car in cars:
        if car.score > best_car.score:
            best_car = car
    return best_car


#this returns the next generation
def get_next_generation(cars):
    best_car = get_best_car(cars).copy()

    del cars

    ret_cars = []
    ret_cars.append(best_car)
    for i in range(1, population_size):
        new_car = best_car.copy()
        new_car.mutate(learning_rate)
        ret_cars.append(new_car)
    return ret_cars
