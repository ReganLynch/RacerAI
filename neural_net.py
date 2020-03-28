#wrapper for tensorflow -> easier neural network manipulation
#this implementation of a neural net has only 1 hidden layer

import tensorflow as tf
import numpy as np
from game_settings import *
import random
import copy


class Neural_Network(object):

    #NEED TO GET RID OF TENSORFLOW WARNING MESSAGES FROM THIS INIT
    def __init__(self, num_input_nodes, num_hidden_nodes, num_output_nodes, model=None):
        self.num_inputs = num_input_nodes
        self.num_hidden = num_hidden_nodes
        self.num_outputs = num_output_nodes
        if not model:
            self.createModel()
        else:
            self.model = model

    def createModel(self):
        hidden = tf.keras.layers.Dense(
            units=self.num_hidden,
            input_shape=(self.num_inputs, ),
            activation='sigmoid')
        output = tf.keras.layers.Dense(
            units=self.num_outputs,
            activation='softmax')
        self.model = tf.keras.Sequential()
        self.model.add(hidden)
        self.model.add(output)

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
