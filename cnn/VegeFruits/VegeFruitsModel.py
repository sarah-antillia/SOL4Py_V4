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

#  CIFARModel.py and
# This is based on the following Keras sample scripts:
# https://gist.github.com/fchollet/0830affa1f7f19fd47b06d4cf89ed44d
#    fchollet/classifier_from_little_data_script_1.py
# and 
# http://www.antillia.com/sol4py/samples/cnn/CIFARClassifier.html
#   CIFARClassififer.py and CIFARModel.py of sol4py
# See also:
# https://keras.io/examples/cifar10_cnn/

# encodig: utf-8

import sys
import os
import cv2
import time
import traceback

import socket
import matplotlib.pyplot as plt
import numpy as np
import keras
 
sys.path.append('../../')

from SOL4Py.ZMain import *
from SOL4Py.ZMLModel import *

from SOL4Py.keras.ZDataSetAugmentor import *
from SOL4Py.keras.ZDataSetLoader import *
from SOL4Py.keras.ZEpochChangeNotifier import *
from SOL4Py.keras.ZSimpleSequentialModel import *

VegeFruits_10  = 0



############################################################
# Classifier Model class


class VegeFruitsModel(ZMLModel):
  WIDTH  = 128
  HEIGHT = 128
  ##
  # Constructor
  def __init__(self, dataset_id, epochs=50, mainv=None, ipaddress="127.0.0.1", port=7777, use_checkpoint_cb=False):
    super(VegeFruitsModel, self).__init__(dataset_id, mainv)
    self._start(self.__init__.__name__)
    
    self.write("dataset_id:{}, ephochs:{}, mainv:{}".format(dataset_id, epochs, mainv) )
    self.model      = None   # Keras model
    self.dataset_id = dataset_id 
    self.dataset    = None
    self.epochs     = epochs
    self.set_dataset_id(dataset_id)
    self.mini_dataset      = ("./mini_dataset", "jpg")
    self.augmented_dataset = ("./augmented_dataset", "png")
    self.image_size = 128 
    self.use_checkpoint_cb = use_checkpoint_cb
    
    self.callbacks  = [ZEpochChangeNotifier(ipaddress, port, self.__class__.__name__, self.epochs+10)]
    
    self._end(self.__init__.__name__)


  def set_dataset_id(self, dataset_id=0):
    self._start(self.set_dataset_id.__name__)
    self.dataset_id   = dataset_id

    self.weight_file  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".h5"
    self.history_file = self.__class__.__name__ + "_" + str(self.dataset_id) + ".history"
    self.nclasses     = 0
    self.write("weight_file  " + self.weight_file)
    self.write("history_file " + self.history_file)
   
    self._end(self.set_dataset_id.__name__)


  def build(self):
    self.write("====================================")
    self._start(self.build.__name__)

    if self.is_trained() != True:

      try:
        self.generate_dataset()
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


  def generate_dataset(self):
    self.augmentor = ZDataSetAugmentor()
    self.n_augmentation = 100
    self.augmentor.generate(self.mini_dataset, self.augmented_dataset, 
        image_size     = self.image_size, 
        n_augmentation = self.n_augmentation)


  def load_dataset(self):
    self._start(self.load_dataset.__name__)
    self.loader    = ZDataSetLoader()

    self.loader.load_dataset(self.augmented_dataset, image_size=self.image_size) 
    self.x_train = self.loader.x_train
    self.y_train = self.loader.y_train
    
    self.x_test  = self.loader.x_test
    self.y_test  = self.loader.y_test
    
    self.n_classes = self.loader.n_classes
    self.classes   = self.loader.classes
    self.save_class_names(self.classes) #2019/09/19
    
    self.loader.show_summary(show_images=False)

    self._end(self.load_dataset.__name__)


  # Create a sequential model
  def create(self):
    self._start(self.create.__name__)
    input_shape = self.x_train.shape[1:]
 
    print(input_shape)
    print(self.n_classes)
    
    self.model = ZSimpleSequentialModel(input_shape, self.n_classes)

    self._end(self.create.__name__)


  def compile(self):
    self._start(self.compile.__name__)
    self.model.compile(optimizer='adam', 
                       loss='categorical_crossentropy', metrics = ['accuracy'])
    self._end(self.compile.__name__)


  def train(self):  
    self._start(self.train.__name__)
    start = time.time()
    print("Epochs " + str(self.epochs))
    print(self.x_train.shape)
    print(self.y_train.shape)

    if (self.use_checkpoint_cb == True) :
      check_point_cb = ModelCheckpoint(self.weight_file, 
                    monitor="acc", verbose=1,
                     save_best_only=True, save_weights_only=True)
      self.callbacks.append(check_point_cb)

    print(self.callbacks)
    
    self.model.history = self.model.fit(self.x_train, self.y_train, 
                         batch_size       = 128,
                         validation_split = 0.2,
                         epochs           = self.epochs,
                         callbacks        = self.callbacks, 
                         verbose          = 1, 
                         shuffle          = True)

    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self.model.summary()
    
    self._end(self.train.__name__)


  def predict(self, image):
    prediction = self.model.predict(image)

    return prediction



  def save(self):
    self._start(self.save.__name__)
        
    self.model.save_weights(self.weight_file)
    self.write("Saved weight file {}".format(self.weight_file))
    self._end(self.save.__name__)
      

  def load(self):
    self._start(self.load.__name__)
  
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
      score = self.model.evaluate(self.x_test, self.y_test, verbose=1)
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




############################################################
#    

if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
   
    dataset_id = VegeFruits_10
    
    epochs     = 20
    if len(sys.argv) ==2:
      epochs = int(sys.argv[1])
 
    print("dataset_id:{} epochs:{}".format(dataset_id, epochs))

    model = VegeFruitsModel(dataset_id, epochs, None,
                         ipaddress="127.0.0.1", port=7777, use_checkpoint_cb=True)
    
    model.build()
 
  except:
    traceback.print_exc()

