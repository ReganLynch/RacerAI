#wrapper for tensorflow -> easier neural network manipulation
#this implementation of a neural net has only 1 hidden layer

import tensorflow as tf
from game_settings import *
import random
import copy


class Neural_Network(object):

    def __init__(self, num_input_nodes, num_hidden_nodes, num_output_nodes, model=None):
        self.num_inputs = num_input_nodes
        self.num_hidden = num_hidden_nodes
        self.num_outputs = num_output_nodes
        if not model:
            self.createModel()
        else:
            self.model = model

    def createModel(self):
        self.model = tf.keras.Sequential([
        #input layer
        tf.keras.layers.Dense(self.num_hidden, activation='relu', input_shape=(self.num_inputs,)),
        #hidden layer
        tf.keras.layers.Dense(self.num_outputs, activation='relu', input_shape=(self.num_inputs,)),
        #output layer
        tf.keras.layers.Dense(self.num_outputs, activation='softmax', input_shape=(self.num_hidden,))
        ])

    def predict(self, inputs):
        ins = np.array([inputs])
        ys = self.model.predict(ins, workers=num_cores, use_multiprocessing=multiprocessing)  #use multi-proccessing if desired
        return ys[0]

    def mutate(self, mutation_rate):
        weights = self.model.get_weights()
        mutated_weights = []
        for i in range(len(weights)):
            tensor = weights[i]
            for j in range(len(tensor)):
                weight = tensor[j]
                if type(weight) is np.ndarray:
                    for x in range(len(weight)):
                        if random.uniform(0, 1) < mutation_rate:
                            weight[x] = weight[x] + random.gauss(0, 1)
                elif random.uniform(0, 1) < mutation_rate:
                    weight = weight + random.gauss(0, 1)
                tensor[j] = weight
            mutated_weights.append(tensor)
        self.model.set_weights(mutated_weights)
