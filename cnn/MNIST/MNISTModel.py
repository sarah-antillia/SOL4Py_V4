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
 
# 2018/09/20

#  MNISTModel.py

# This is based on the following sample program.
# https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py
# See also https://keras.io/datasets/

# encodig: utf-8

import sys
import os
import time
import traceback

import numpy as np

import keras
import tensorflow as tf
from keras.utils import np_utils
from keras.models import Sequential

from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint

#from keras.datasets import mnist, 
from keras import backend as K
from keras.models import model_from_json

 
sys.path.append('../../')

from SOL4Py.ZMLModel import *
from SOL4Py.ZMain    import *


MNIST         = 0
FASHION_MNIST = 1

############################################################
# Classifier Model clas

class MNISTModel(ZMLModel):


  ##
  # Constructor
  def __init__(self, dataset_id, epochs=5, mainv=None):
    super(MNISTModel, self).__init__(dataset_id, mainv)
    self.write("====================================")
    self._start(self.__init__.__name__)

    self.model_filepath   = None
    self.weight_filepath  = None

    self.X_train = None
    self.y_train = None
    
    self.X_test  = None
    self.y_test  = None

    self.image_rows = 28 
    self.image_cols = 28
    
    self.set_input_shape()
    
    self.nclasses = 10

    self.epochs   = epochs
    self.batch_size = 128

    self.set_model_filename()

    self._end(self.__init__.__name__)
 
 
  def build(self):
    self._start(self.build.__name__)
    try:
      self.load_dataset()
      self.create()
              
      if self.is_trained():
        self.load() 
        self.compile()
        
      else:
        self.compile()
        self.train()
        self.save()

      self.evaluate()

    except:
      traceback.print_exc()

    self._end(self.build.__name__)


  def set_input_shape(self):
    self.write("Image data_format:{}".format(K.image_data_format()))

    if K.image_data_format() == 'channels_first':
      self.input_shape = (1, self.image_rows, self.image_cols)
    else:
      self.input_shape = (self.image_rows, self.image_cols, 1)


  def set_dataset_id(self, dataset_id):
    self.dataset_id = dataset_id
    self.set_model_filename()
    #self.model = None


  def load_dataset(self):
    self._start(self.load_dataset.__name__)
    
    if self.dataset_id == MNIST:
      (self.X_train, self.y_train), (self.X_test, self.y_test) = keras.datasets.mnist.load_data()
      self.write("Loaded mnist dataset")
      
    if self.dataset_id == FASHION_MNIST:
      (self.X_train, self.y_train), (self.X_test, self.y_test) = keras.datasets.fashion_mnist.load_data()
      self.write("Loaded fashion_mnist dataset")
 
    if K.image_data_format() == 'channels_first':
      self.X_train = self.X_train.reshape(self.X_train.shape[0], 1, self.image_rows, self.image_cols)
      self.X_test  = self.X_test. reshape(self.X_test.shape[0],  1, self.image_rows, self.image_cols)
    else:
      self.X_train = self.X_train.reshape(self.X_train.shape[0], self.image_rows, self.image_cols, 1)
      self.X_test  = self.X_test. reshape(self.X_test.shape[0],  self.image_rows, self.image_cols, 1)
      
    self.X_train = self.X_train.astype('float32') / 255.0
    self.X_test  = self.X_test. astype('float32') / 255.0

    # convert class vectors to binary class matrices
    self.y_train = keras.utils.to_categorical(self.y_train, self.nclasses)
    self.y_test  = keras.utils.to_categorical(self.y_test,  self.nclasses)

    self._end(self.load_dataset.__name__)


  def create(self):
    self._start(self.create.__name__)

    self.model = Sequential()
    self.model.add(Conv2D(32, (3, 3), padding = 'same', input_shape = self.input_shape))
    self.model.add(Activation('relu'))

    self.model.add(Conv2D(64, (3, 3), padding='same'))
    self.model.add(Activation('relu'))

    self.model.add(MaxPooling2D(pool_size=(2, 2)))
    self.model.add(Dropout(0.25))
    
    self.model.add(Flatten())
    self.model.add(Dense(128))
    self.model.add(Activation('relu'))

    self.model.add(Dropout(0.5))

    self.model.add(Dense(self.nclasses))

    self.model.add(Activation('softmax'))
        
    self._end(self.create.__name__)


  def compile(self):
    self._start(self.compile.__name__)

    self.model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    
    self._end(self.compile.__name__)


  def train(self):  
    self._start(self.train.__name__)
    start = time.time()
    self.model.fit(self.X_train, self.y_train, 
                   batch_size=self.batch_size, epochs=self.epochs,
                   validation_split=0.1, verbose=1)

    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self._end(self.train.__name__)


  def evaluate(self):
    self._start(self.evaluate.__name__)
    try:
      score = self.model.evaluate(self.X_test, self.y_test, verbose=0)
      self.write("Test loss    :{}".format(score[0]))     
      self.write("Test accuracy:{}".format(score[1]))

    except:
      self.write(formatted_traceback())
      
    self._end(self.evaluate.__name__)


  def plot(self, filename=None):
    from keras.utils import plot_model
    if filename == None:
       filename = self.__class__.__name__ + "_model.png"
    plot_model(self.model, to_file=filename,show_shapes=True)

  # Remove model file and weight file.
  def clear(self):
    if self.trained():
      os.remove(self.model_filepath)
      os.remove(self.weight_filepath)
      self.model = None


  def set_model_filename(self):
    self._start(self.set_model_filename.__name__)

    model_file  = self.__class__.__name__ + "_"  + str(self.dataset_id) + ".json"
    weight_file = self.__class__.__name__ + "_"  + str(self.dataset_id) + ".h5"
 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    self.model_file  = os.path.join(current_dir, model_file)
    self.weight_file = os.path.join(current_dir, weight_file)
    self.write("ModelFile  " + self.model_file)
    self.write("WeightFile " + self.weight_file)
    self._end(self.set_model_filename.__name__)


  def is_trained(self):
    self._start(self.trained.__name__)
    rc = False
  
    if os.path.isfile(self.model_file) == True and os.path.isfile(self.weight_file) == True:
      self.write("Found model file:'{}', and weight_file:'{}'".format(self.model_file, self.weight_file))

      rc = True
    self._end(self.trained.__name__)
    
    return rc


  def save(self):
    self._start(self.save.__name__)
 
    try: 
      with open(self.model_file, "w") as file:
        file.write(self.model.to_json())
        
        self.write("Saved model file {}".format(self.model_file))
        
      self.model.save_weights(self.weight_file)
      self.write("Saved weight file {}".format(self.weight_file))

    except:
      print(formatted_traceback())
  
    self._end(self.save.__name__)


  def load(self):
    self._start(self.load.__name__)
    try:
      if os.path.isfile(self.model_file) == True and os.path.isfile(self.weight_file) == True:
        self.write("Try to load model and weight:\n {}\n {}".format(self.model_file, self.weight_file))
    
        with open(self.model_file,'r') as file:
          json = file.read()
          self.model = model_from_json(json)
          self.write("Loaded model_file " + self.model_file)
      
        self.model.load_weights(self.weight_file)
        self.write("Loaded weight file " + self.weight_file)
      else:
        self.write("Not found model and weight files")
    except:
      self.write(formatted_traceback())
        
    self._end(self.load.__name__)


  def predict(self, image):
    preds  = self.model.predict(image)
    return preds


  def predict_classes(self, image):
    self._start(self.predict_classes.__name__)
    classes  = self.model.predict_classes(image)
    self._end(self.predict_classes.__name__)
    return classes
    

  def predict_prob(self, image):
    self._start(self.predict_prob.__name__)
    prob  = self.model.predict_prob(image)
    self._end(self.predict_prob.__name__)
    return prob


############################################################
#
#

if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
   
    dataset_id = MNIST
    epochs     = 10
    
    if len(sys.argv) >= 2:
      dataset_id = int(sys.argv[1])
    if len(sys.argv) >= 3:
      epochs = int(sys.argv[2])
     
    print("dataset_id:{} epochs:{}".format(dataset_id, epochs))
        
    if dataset_id == MNIST or dataset_id == FASHION_MNIST :
      model = MNISTModel(dataset_id, epochs, None)
      model.build()
    else:
      print("Invalid dataset_id: {}".format(dataset_id))

  except:
    traceback.print_exc()

    
    