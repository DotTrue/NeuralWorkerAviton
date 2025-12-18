
import random

import GUI
import tkinter as tk
from  PIL import Image, ImageTk, ImageDraw
import matplotlib.pyplot
import numpy as np
import sklearn
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Flatten
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
import matplotlib.pyplot as plt
from keras.datasets import mnist
(lrn_task,learn_answr),(test_task,test_answr) = mnist.load_data()

test_task = test_task / 255
lrn_task = lrn_task / 255

print(lrn_task)
learn_answr = keras.utils.to_categorical(learn_answr,10)
test_answr = keras.utils.to_categorical(test_answr,10)
model = Sequential([Flatten(input_shape=(28,28,1)),Dense(200,activation="relu"),Dense(10,activation="softmax")])
model.compile(optimizer=Adam(),loss="categorical_crossentropy",metrics=["accuracy"])
model.fit(lrn_task,learn_answr,epochs=10,batch_size=25,validation_data=(test_task,test_answr))





def Predict(matrix):
    matrix = matrix.reshape(-1,28,28,1)
    result = model.predict(matrix)
    print(result,"RES")
    number = np.argmax(result)
    percentage = round(np.max(result) * 100)
    print(number, percentage)
    return number,percentage

