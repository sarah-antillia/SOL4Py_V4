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

#  CIFARAutoEncoderModel.py

# encodig: utf-8

import sys
import os
import time
import traceback

import matplotlib.pyplot as plt
import numpy as np

import keras
import tensorflow as tf
from keras.utils import np_utils
#from keras import backend as K
from keras.models import model_from_json
from keras.datasets import cifar10, cifar100


sys.path.append('../../')

from SOL4Py.ZMLModel import *
from SOL4Py.ZMain    import *

from SOL4Py.keras.ZEpochChangeNotifier import *
from SOL4Py.keras.ZSimpleAutoEncoderModel import *

# cifar dataset id
CIFAR10    = 0
CIFAR100   = 1

class CIFARAutoEncoder(ZMLModel):

  IMAGE_SIZE = 32
  CHANNELS   = 3
  
  ################
  #Inner class 
  
  class CIFARAutoEncoderModel(ZSimpleAutoEncoderModel):
  
    # Construcotr
    def __init__(self, input_shape):
      ZSimpleAutoEncoderModel.__init__(self, input_shape)


    def encode(self, input_image):
      x = Conv2D(64, (3, 3), activation='relu', padding='same')(input_image)
      x = MaxPooling2D((2, 2),                  padding='same')(x)
      x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
      x = MaxPooling2D((2, 2),                  padding='same')(x)
      x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
      encoded = MaxPooling2D((2, 2),            padding='same')(x)
      return encoded


    def decode(self, encoded):
      x = Conv2D(16, (3, 3), activation='relu',         padding='same')(encoded)
      x = UpSampling2D((2, 2))(x)
      x = Conv2D(32, (3, 3), activation='relu',         padding='same')(x)
      x = UpSampling2D((2, 2))(x)
      x = Conv2D(64, (3, 3), activation='relu',         padding='same')(x)
      x = UpSampling2D((2, 2))(x)
      decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)
      return decoded


  ##
  # Constructor
  def __init__(self, dataset_id = CIFAR10, 
                     epochs=20, view=None, ipaddress="127.0.0.1", port=8888):
    super(CIFARAutoEncoder, self).__init__(0, view)

    self.input_shape =(self.IMAGE_SIZE, self.IMAGE_SIZE, self.CHANNELS) 

    self.epochs      = epochs
    self.dataset_id  = dataset_id
    
    # The following callbacks will be used to train AutoEncoderModel
    self.callbacks = [ZEpochChangeNotifier(ipaddress, port, self.__class__.__name__+str("-") + str(self.dataset_id), 
                self.epochs+10)]

    self.set_weight_filepath()


  def build(self):
    self._start(self.build.__name__)
    try:
      # 1 Load cifar dataset
      self.load_dataset()
      
      # 2 Create a cifar AutoEncoderModel
      self.create()

      if self.is_trained():
        # 3 If our cifar model trained, i.e, if weight_filepath.h5 exists
        self.load() 
        self.compile()
      else:
        self.compile()
        self.train()
        self.save()
        
    except:
      traceback.print_exc()
      
    self._end(self.build.__name__)


  def set_weight_filepath(self):
    self._start(self.set_weight_filepath.__name__)
    self.weight_filepath  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".h5"
    self.write("weight_file  " + self.weight_filepath)

    self._end (self.set_weight_filepath.__name__)


  def load_dataset(self):
    self._start(self.load_dataset.__name__)
    
    # We don't need labels y_train and y_test.
    if (self.dataset_id == CIFAR10):
      (x_train, _), (x_test, _) = cifar10.load_data()
    if (self.dataset_id == CIFAR100):
      (x_train, _), (x_test, _) = cifar100.load_data()

    self.x_train = x_train.astype('float32') / 255.
    self.x_test  = x_test. astype('float32') / 255.

    #self.x_train = np.reshape(x_train, (len(x_train), 
    #                     self.IMAGE_SIZE, self.IMAGE_SIZE, self.CHANNELS)) 
    #self.x_test  = np.reshape(x_test, (len(x_test), 
    #                     self.IMAGE_SIZE, self.IMAGE_SIZE, self.CHANNELS)) 
    self._end (self.load_dataset.__name__)


  def create(self):
    self._start(self.create.__name__)
    self.model = self.CIFARAutoEncoderModel(self.input_shape)
    self._end (self.create.__name__)


  def compile(self):
    self._start(self.compile.__name__)
    self.model.compile(optimizer='adadelta', loss='binary_crossentropy')
    self._end (self.compile.__name__)


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
    self._start(self.is_trained.__name__)
    rc = False
    if os.path.isfile(self.weight_filepath) == True:
      print("weight filename {}".format(self.weight_filepath))
      rc = True
 
    self._end(self.is_trained.__name__)
    return rc


  def predict(self): 
    self._start(self.predict.__name__)
    # Call self.model.predict method to get decoded_images from x_test image
    self.decoded_images = self.model.predict(self.x_test)
    self._end(self.predict.__name__)


  def load(self):
    self._start(self.load.__name__)
    if os.path.isfile(self.weight_filepath) == True:

      try:
    
        self.model.load_weights(self.weight_filepath)
        self.write("Loaded a weight file:{}".format(self.weight_filepath))
      except:
        self.write( formatted_traceback() )
    else:
      raise Exception("Not found weight file{: {}".format(self.weight_filepath))
      
    self._end(self.load.__name__)


  def show_images(self, n=10):
    fig = plt.figure() #figsize=(20, 4))
    for i in range(1, n+1):
      # Display original x_test images
      ax = plt.subplot(2, n, i)
      plt.imshow(self.x_test[i].reshape(self.IMAGE_SIZE, self.IMAGE_SIZE, self.CHANNELS))
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)

      # Display decoded images predicted from original x_test images. 
      ax = plt.subplot(2, n, i + n)
      plt.imshow(self.decoded_images[i].reshape(self.IMAGE_SIZE, self.IMAGE_SIZE, self.CHANNELS))
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
   
    epochs     = 20
    if len(sys.argv) ==2:
      epochs = int(sys.argv[1])

    model = CIFARAutoEncoder(dataset_id= CIFAR10, 
                                  epochs= epochs)
    model.build()
    
    model.predict()
    model.show_images()
    
  except:
    traceback.print_exc()

