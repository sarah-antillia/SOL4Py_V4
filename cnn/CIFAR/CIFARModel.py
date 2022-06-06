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
# 2019/05/05 Updated to use ZSimpleSequentialModel and ZEpochChangeNotifier


#  CIFARModel.py

# encodig: utf-8

import sys
import os
import cv2
import time
import traceback
import pandas as pd
import seaborn as sns
import socket
import matplotlib.pyplot as plt
import numpy as np
import keras

from keras.models import Sequential, model_from_json

#from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
from keras.datasets import cifar10, cifar100

from keras.utils import np_utils
 
sys.path.append('../../')

from SOL4Py.ZMain import *
from SOL4Py.ZMLModel import *

from SOL4Py.keras.ZEpochChangeNotifier import *
from SOL4Py.keras.ZSimpleSequentialModel      import *
from SOL4Py.keras.ZEpochChangeNotifier import *

CIFAR10  = 0
CIFAR100 = 1



############################################################
# Classifier Model class

class CIFARModel(ZMLModel):
  ##
  # Constructor
  def __init__(self, dataset_id, epochs=0, mainv=None, ipaddress="127.0.0.1", port=7777):
    super(CIFARModel, self).__init__(0, mainv)

    #self.view   = mainv
    self._start(self.__init__.__name__)
    
    self.write("dataset_id:{}, ephochs:{}, mainv:{}".format(dataset_id, epochs, mainv) )
    self.ipaddress = ipaddress
    self.port      = port 
    self.model     = None   # Keras model
    self.dataset_id = dataset_id  # CIFAR10 or CIFAR100
    self.dataset   = None
    self.epochs    = epochs
    self.set_dataset_id(dataset_id)
    
    self.callbacks = [ZEpochChangeNotifier(ipaddress, port, self.__class__.__name__+str("-") + str(self.dataset_id), self.epochs+10)]

    self._end(self.__init__.__name__)


  def set_dataset_id(self, dataset_id):
    self._start(self.set_dataset_id.__name__)
    self.dataset_id   = dataset_id
    
    self.weight_file  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".h5"
    #self.history_file = self.__class__.__name__ + "_" + str(self.dataset_id) + ".history"
    self.nclasses     = 0
    self.write("weight_file  " + self.weight_file)
    #self.write("history_file " + self.history_file)
   
    self._end(self.set_dataset_id.__name__)



  def build(self):
    self.write("====================================")
    self._start(self.build.__name__)
    
    if self.is_trained() != True:
      try:
        self.load_dataset()
        self.create()
        self.compile()
      
        self.train()
        self.evaluate()
        self.save()
        self.plot()

      except:
        traceback.print_exc()
    
    self._end(self.build.__name__)


  #
  def load_dataset(self):
    self._start(self.load_dataset.__name__)
    # Load CIFAR-10
    
    if self.dataset_id == CIFAR10:
      (self.X_train, self.y_train), (self.X_test, self.y_test) = cifar10.load_data()
      self.nclasses = 10
      
    if self.dataset_id == CIFAR100:
      (self.X_train, self.y_train), (self.X_test, self.y_test) = cifar100.load_data(label_mode='fine') #2019/05/05 Added label_mode
      self.nclasses = 100
      
    # Normalize data
    self.X_train = self.X_train.astype('float32')/255.0
    self.X_test  = self.X_test. astype('float32')/255.0

    # Onehot label
    self.y_train = np_utils.to_categorical(self.y_train, self.nclasses)
    self.y_test  = np_utils.to_categorical(self.y_test,  self.nclasses)

    self._end(self.load_dataset.__name__)


  # Create a sequential model
  def create(self):
    self._start(self.create.__name__)
    self.image_size = (32, 32, 3)
    
    self.model = ZSimpleSequentialModel(self.image_size, self.nclasses)

    self._end(self.create.__name__)
 

  def compile(self):
    self._start(self.compile.__name__)  
    self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics = ['accuracy'])
    self._end(self.compile.__name__)


  def train(self):  
    self._start(self.train.__name__)
    start = time.time()
    print(self.X_train.shape)
    print(self.y_train.shape)
    
    self.model.history = self.model.fit(self.X_train, self.y_train, 
                         batch_size=128, epochs=self.epochs, verbose=1, 
                         callbacks = self.callbacks, 
                         validation_split=0.1)
    
    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self.model.summary()
    self._end(self.train.__name__)


  def predict(self, image):
    #self._start(self.predict.__name__)
    
    prediction = self.model.predict(image)
    
    #self.write("Prediction: {}".format(prediction))
 
    #self._end(self.predict.__name__)
    return prediction
 

  def predict_classes(self, image):
    self._start(self.predict_classes.__name__)
    classes = self.model.predict_classes(image)
    self.write("Predicted classes{}".format(classes))
    self._end(self.predict_classes.__name__)
    return classes


  def save(self):
    self._start(self.save.__name__)

    self.model.save_weights(self.weight_file)
    self.write("Saved weight file {}".format(self.weight_file))
    self._end(self.save.__name__)
      

  def load(self):
    self._start(self.load.__name__)
    print("Load weight {}".format(self.weight_file))
    try:                
      self.model.load_weights(self.weight_file)
      self.write("Loaded a weight file:{}".format(self.weight_file))

    except:
      self.write( formatted_traceback() )

    self._end(self.load.__name__)


  def get_model(self):
    return self.model


  def is_trained(self):
    rc = False
    
    if os.path.isfile(self.weight_file) == True:
      self.write("Found weight_file:'{}'".format(self.weight_file))
      rc = True
    return rc


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
    plot_model(self.model, to_file=filename, show_shapes=True)


        
############################################################
#    

if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
   
    dataset_id = CIFAR10
    epochs     = 20 #2019/04/25
    
    if len(sys.argv) >= 2:
      dataset_id = int(sys.argv[1])
      
    if len(sys.argv) >= 3:
      epochs = int(sys.argv[2])
     
    print("dataset_id:{} epochs:{}".format(dataset_id, epochs))
    
    
    if dataset_id == CIFAR10 or dataset_id == CIFAR100 :
      model = CIFARModel(dataset_id, epochs, None)
      model.build()
    else:
      print("Invalid dataset_id: {}".format(dataset_id))

  except:
    traceback.print_exc()

