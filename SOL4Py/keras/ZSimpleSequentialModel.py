# Copyright 2020-2021 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 2019/04/30 

#  ZSimpleSequentialModel.py

# encodig: utf-8
import os
import sys

import keras

#from keras.models import Sequential
import tensorflow as tf
from tensorflow.keras.models import Sequential
#from keras.layers import *
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

# This is a very simple Keras Deep CNN sequential model derived from keras.models.Sequentail
 
# See: https://keras.io/examples/cifar10_cnn/

#class ZSimpleSequentialModel(keras.models.Sequential):
class ZSimpleSequentialModel(Sequential):

  ##
  # Constructor
  def __init__(self, input_shape, n_classes):
    super(ZSimpleSequentialModel, self).__init__()

    # Create a sequential model, and add keras.layers.* to the model
    self.add(Conv2D(32, kernel_size=(3, 3),  padding = 'same', input_shape = input_shape))
    self.add(Activation('relu'))
    
    self.add(Conv2D(32, kernel_size=(3, 3), padding = 'same'))
    self.add(Activation('relu'))
    
    #self.add(MaxPool2D(pool_size = (2, 2)))
    self.add(MaxPooling2D(pool_size = (2, 2)))
  
    self.add(Dropout(0.25))

    self.add(Conv2D(64, kernel_size=(3, 3), padding = 'same'))
    self.add(Activation('relu'))

    self.add(Conv2D(64, kernel_size=(3, 3), padding = 'same')) 
    self.add(Activation('relu'))

    #self.add(MaxPool2D(pool_size = (2, 2)))
    self.add(MaxPooling2D(pool_size = (2, 2)))

    self.add(Dropout(0.25))

    self.add(Flatten())
    self.add(Dense(512))
    self.add(Activation('relu'))
    self.add(Dropout(0.5))
    
    self.add(Dense(n_classes))
    
    self.add(Activation('softmax'))


