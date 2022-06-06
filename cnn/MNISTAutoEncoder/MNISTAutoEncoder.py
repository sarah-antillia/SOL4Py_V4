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

# 2019/05/10

#  MNISTAutoEncoderModel.py

# This is based on the following sample program.
# https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py
# See also https://keras.io/datasets/

# encodig: utf-8

import sys
import os
import time
import traceback
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np

#import keras
import tensorflow as tf
from tensorflow.python.keras.utils import np_utils

from tensorflow.python.keras.datasets import mnist
#from keras import backend as K
from tensorflow.python.keras.models import model_from_json

import numpy as np

sys.path.append('../../')

from SOL4Py.ZMLModel import *
from SOL4Py.ZMain    import *

from SOL4Py.keras.ZEpochChangeNotifier       import *
from SOL4Py.keras.ZSimpleAutoEncoderModel import *


class MNISTAutoEncoder(ZMLModel):

  IMAGE_SIZE = 28
  CHANNELS   = 1    #1: Gray scale

  ##
  # Constructor

  def __init__(self, epochs, mainv=None, ipaddress="127.0.0.1", port=8888):
    super(MNISTAutoEncoder, self).__init__(0, mainv)

    self.input_shape =(self.IMAGE_SIZE, self.IMAGE_SIZE, self.CHANNELS) 

    self.epochs = epochs
    self.dataset_id = 0
    self.callbacks = [ZEpochChangeNotifier(ipaddress, port, self.__class__.__name__+str("-") + str(self.dataset_id), 
                self.epochs+10)]
    self.set_weight_filepath()


  def build(self):
    self._start(self.build.__name__)
    try:
      # 1. Load MNIST dataset
      self.load_dataset()
      
      # 2. Cread MNISTAutoEncoderModel
      self.create()

      if self.is_trained():
        # 3. If our model already trained, load the model's weight file.
        self.load()
        
        # 4. Compile
        self.compile()

      else:
        # 5. If not trained
        self.compile()
        
        # 6. Train MNISTAutoEncoderModel
        self.train()
        
        # 7. Save the weight file
        self.save()

    except:
      traceback.print_exc()

    self._end(self.build.__name__)


  def set_weight_filepath(self):
    self._start(self.set_weight_filepath.__name__)

    weight_file = self.__class__.__name__ + "_"  + str(self.dataset_id) + ".h5"
 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    self.weight_filepath = os.path.join(current_dir, weight_file)
    self.write("WeightFilePath " + self.weight_filepath)
    self._end(self.set_weight_filepath.__name__)


  def load_dataset(self):
    (x_train, _), (x_test, _) = mnist.load_data()

    x_train = x_train.astype('float32') / 255.
    x_test  = x_test. astype('float32') / 255.
    self.x_train = np.reshape(x_train, (len(x_train), 
                         self.IMAGE_SIZE, self.IMAGE_SIZE, self.CHANNELS)) 
    self.x_test  = np.reshape(x_test, (len(x_test), 
                         self.IMAGE_SIZE, self.IMAGE_SIZE, self.CHANNELS)) 


  def create(self):
    self._start(self.create.__name__)
    self.model = ZSimpleAutoEncoderModel(self.input_shape)
    self._end(self.create.__name__)


  def compile(self):
    self._start(self.compile.__name__)
    self.model.compile(optimizer='adadelta', loss='binary_crossentropy')
    self._end(self.compile.__name__)


  def train(self):  
    self._start(self.train.__name__)
    start = time.time()

    self.model.fit(self.x_train, self.x_train,
                epochs= self.epochs,
                batch_size=128,
                shuffle=True,
                verbose=True,
                validation_data=(self.x_test, self.x_test),
                callbacks = self.callbacks
                )
    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self._end(self.train.__name__)



  def is_trained(self):
    self._start(self.trained.__name__)
    rc = False
    # Does the weight_file exist? 
    if os.path.isfile(self.weight_filepath) == True:
      rc = True
 
    self._end(self.trained.__name__)
    return rc


  def predict(self):
    # Call self.model.predict method to get decoded_images from x_test image
    self.decoded_images = self.model.predict(self.x_test)


  def load(self):
    self._start(self.load.__name__)
    
    try:
      self.model.load_weights(self.weight_filepath)
      self.write("Loaded a weight file:{}".format(self.weight_filepath))
    except:
      self.write( formatted_traceback() )

    self._end(self.load.__name__)


  def show_images(self, n=10):

    fig = plt.figure(figsize=(20, 4))
    for i in range(1, n+1):
        # Display original x_test images
        ax = plt.subplot(2, n, i)
        plt.imshow(self.x_test[i].reshape(self.IMAGE_SIZE, self.IMAGE_SIZE))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Display decoded images predicted from original x_test images. 
        ax = plt.subplot(2, n, i + n)
        plt.imshow(self.decoded_images[i].reshape(self.IMAGE_SIZE, self.IMAGE_SIZE))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    fig.tight_layout()
    plt.show()


  def save(self):
    self._start(self.save.__name__)
    try:         
      self.model.save_weights(self.weight_filepath)
      self.write("Saved weight file {}".format(self.weight_filepath))
    except:
      print(formatted_traceback())
  
    self._end(self.save.__name__)


#################################################
#
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])

    epochs     = 10
    if len(sys.argv) == 2:
      epochs = int(sys.argv[1])

    model = MNISTAutoEncoder(epochs)
    model.build()
    
    model.predict()
    
    model.show_images()
    
  except:
    traceback.print_exc()

