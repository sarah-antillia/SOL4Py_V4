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

# 2019/05/13

# TOKYO2020_SPORT_PICTOGRAMS_Model.py

# encodig: utf-8

import sys
import os
import time
import traceback

import matplotlib.pyplot as plt
import numpy as np
import keras
#from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

#from keras import backend as K
#from keras.utils import np_utils
 
sys.path.append('../../')

from SOL4Py.ZMain    import *
from SOL4Py.ZMLModel import *

from SOL4Py.keras.ZSimpleSequentialModel import *
from SOL4Py.keras.ZEpochChangeNotifier import *


############################################################
# Pictogram Model class based on Keras ImageDataGenerator.


class TOKYO2020_SPORT_PICTOGRAMS_Model(ZMLModel):

  ## Class Variables
  IMAGE_MODEL  = 0

  IMAGE_WIDTH    = 64
  IMAGE_HEIGHT   = 64
  IMAGE_CHANNELS = 3

  TRAIN_DATA_DIR = "./dataset/train"
  VALID_DATA_DIR = "./dataset/valid"

  ##
  # Constructor
  def __init__(self, dataset_id, epochs=10, mainv=None, ipaddress="127.0.0.1", port=7777):
    super(TOKYO2020_SPORT_PICTOGRAMS_Model, self).__init__(dataset_id, mainv)
    
    self._start(self.__init__.__name__)
    
    self.write("dataset_id:{}, ephochs:{}, mainv:{}".format(dataset_id, epochs, mainv) )
    self.model      = None   # Keras model
    self.dataset_id = dataset_id 
    self.dataset    = None
    self.epochs     = epochs
    self.set_dataset_id(dataset_id)

    self.callbacks = [ZEpochChangeNotifier(ipaddress, port, self.__class__.__name__, self.epochs+10)]
    try:
      self.classes   = sorted( os.listdir(self.TRAIN_DATA_DIR) )
      self.save_class_names(self.classes) #2019/09/20
      self.n_classes = len(self.classes)

    except:
      self.classes   = None
      self.n_classes = 0    

    self.image_width    = self.IMAGE_WIDTH
    self.image_height   = self.IMAGE_HEIGHT
    self.image_channels = self.IMAGE_CHANNELS
    
    self.IMAGE_SIZE = (self.image_width, self.image_height)

    self._end(self.__init__.__name__)


  def set_dataset_id(self, dataset_id):
    self._start(self.set_dataset_id.__name__)
    self.dataset_id   = dataset_id
    
    self.weight_filepath  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".h5"
    self.write("weight_filepath  " + self.weight_filepath)
   
    self._end(self.set_dataset_id.__name__)


  def build(self):
    self.write("====================================")
    self._start(self.build.__name__)

    # If no weight file to our model were found , the model is not trained.
    if self.is_trained() != True:
      try:
        
        # Create ImageDataGenerator
        self.create_generator()
        
        self.create_flow()
        
        self.create()
        self.compile()
        
        self.train()
  
        self.save()
        self.plot()

      except:
        traceback.print_exc()
      
    self._end(self.build.__name__)


  # Create two image data generator for training and validation.
  def create_generator(self):
    self._start(self.create_generator.__name__)
    
    # 1. Create a training data generator. Do image rescaling and augmentation. 
    self.train_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
                                        rescale            = 1.0/255.0,
                                        rotation_range     = 20,    
                                        width_shift_range  = 1.0, 
                                        height_shift_range = 0.3,
                                        shear_range        = 0.4,       
                                        zoom_range         = 0.3,        
                                        brightness_range   = [0.7,1.2],
                                        channel_shift_range= 2.0, 
                                        horizontal_flip    = False,
                                        vertical_flip      = False)

    # 2. Create a validation data generator. Rescaling only, no augmentation needed.
    self.valid_data_generator  = tf.keras.preprocessing.image.ImageDataGenerator( 
                                        rescale            = 1.0/255.0)

    self._end(self.create_generator.__name__)


  # Create two image data flow from to use a training an validation.
  def create_flow(self):
    self._start(self.create_flow.__name__)
    self.BATCH_SIZE = 32
    self.CLASS_MODE = "categorical"
    self.COLOR_MODE = "rgb"   #grayscale

    self.train_flow = self.train_data_generator.flow_from_directory(
         self.TRAIN_DATA_DIR,
         target_size = self.IMAGE_SIZE,
         batch_size  = self.BATCH_SIZE,
         class_mode  = self.CLASS_MODE,
         color_mode  = self.COLOR_MODE,
         shuffle     = True)

    self.valid_flow = self.valid_data_generator.flow_from_directory(
         self.VALID_DATA_DIR,
         target_size = self.IMAGE_SIZE,
         batch_size  = self.BATCH_SIZE,
         class_mode  = self.CLASS_MODE,
         color_mode  = self.COLOR_MODE,
         shuffle     = True)

    self._end(self.create_flow.__name__)


  # Create a sequential model
  def create(self):
    self._start(self.create.__name__)
    input_shape = (self.image_width, self.image_height, self.image_channels)
    self.model = ZSimpleSequentialModel(input_shape, self.n_classes)
    self._end(self.create.__name__)


  # Compile self.model.
  def compile(self):
    self._start(self.compile.__name__)  
    self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics = ['accuracy'])
    self._end(self.compile.__name__)


  # Train an validate self.model by using fit_generator method of self.model.
  def train(self, train_steps =100, valid_steps = 20):  
    self._start(self.train.__name__)
    start = time.time()

    self.train_steps = train_steps
    self.valid_steps = valid_steps

    self.model.fit_generator(
             self.train_flow,
             steps_per_epoch  = self.train_steps,      
             epochs           = self.epochs,
             callbacks        = self.callbacks,
             validation_data  = self.valid_flow,
             validation_steps = self.valid_steps)
    
    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self.model.summary()
    self._end(self.train.__name__)


  # Predict classes of the image. 
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

  # Save the model to self.weith_filepath.
  def save(self):
    self._start(self.save.__name__)
        
    self.model.save_weights(self.weight_filepath)
    self.write("Saved weight file {}".format(self.weight_filepath))
    self._end(self.save.__name__)


  # Load a weight from self.weight_filepaht into sefl.model.
  def load(self):
    self._start(self.load.__name__)

    try:                
      self.model.load_weights(self.weight_filepath)
      self.write("Loaded a weight file:{}".format(self.weight_filepath))

    except:
      self.write( formatted_traceback() )

    self._end(self.load.__name__)


  def get_model(self):
    return self.model


  def is_trained(self):
    rc = False
    
    if os.path.isfile(self.weight_filepath) == True:
      rc = True
    return rc


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
   
    dataset_id = TOKYO2020_SPORT_PICTOGRAMS_Model.IMAGE_MODEL
    
    epochs     = 10

    if len(sys.argv) >= 2:
      dataset_id = int(sys.argv[1])
      
    if len(sys.argv) >= 3:
      epochs = int(sys.argv[2])

    model = TOKYO2020_SPORT_PICTOGRAMS_Model(dataset_id, epochs, None)
    model.build()

  except:
    traceback.print_exc()

