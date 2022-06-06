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


# encodig: utf-8

import sys
import os
import time
import traceback
import socket
import matplotlib.pyplot as plt
import numpy as np
#import keras

#from keras.preprocessing.image import ImageDataGenerator

#from keras import backend as K

#from keras.utils import np_utils

from tensorflow.python.keras.utils import np_utils

from tensorflow.keras.models import Sequential
#from keras.layers import *
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

 
sys.path.append('../../')

from SOL4Py.ZMain import *
from SOL4Py.ZMLModel import *

from SOL4Py.keras.ZDataSetAugmentor import *
from SOL4Py.keras.ZDataSetLoader import *
from SOL4Py.keras.ZEpochChangeNotifier import *
from SOL4Py.keras.ZSimpleAutoEncoderModel import *

VegeFruits_10  = 0



############################################################
# Classifier Model class


class VegeFruitsAutoEncoder(ZMLModel):
  IMAGE_SIZE = 128
  CHANNELS   = 3
  
  ################
  #Inner class to define VegeFruitsAutoEncoderMode which inherits ZSimpleAutoEncoderModel
  class VegeFruitsAutoEncoderModel(ZSimpleAutoEncoderModel):
  
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
  def __init__(self, dataset_id, epochs=50, mainv=None, ipaddress="127.0.0.1", port=7777, use_checkpoint_cb=False):
    super(VegeFruitsAutoEncoder, self).__init__(dataset_id, mainv)
    self._start(self.__init__.__name__)
    
    self.write("dataset_id:{}, ephochs:{}, mainv:{}".format(dataset_id, epochs, mainv) )
    self.model      = None   # Keras model
    self.dataset_id = dataset_id 
    self.dataset    = None
    self.epochs     = epochs
    self.dataset_id = dataset_id
    
    self.mini_dataset      = ("./mini_dataset", "jpg")
    self.augmented_dataset = ("./augmented_dataset", "png")
    self.image_size = self.IMAGE_SIZE 
    self.use_checkpoint_cb = use_checkpoint_cb
    
    self.callbacks  = [ZEpochChangeNotifier(ipaddress, port, self.__class__.__name__, self.epochs+10)]
    self.set_weight_filepath()
    
    self._end(self.__init__.__name__)


  def set_weight_filepath(self):
    self._start(self.set_weight_filepath.__name__)
    weight_file = self.__class__.__name__ + "_"  + str(self.dataset_id) + ".h5"
    current_dir = os.path.dirname(os.path.abspath(__file__))

    self.weight_filepath = os.path.join(current_dir, weight_file)
    self.write("WeightFilePath " + self.weight_filepath)
    self._end(self.set_weight_filepath.__name__)


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
        self.save()
         
      except:
        traceback.print_exc()
    else:
      #  If our cifar model trained, i.e, if weight_filepath.h5 exists
      self.load_dataset()

      self.create()
      self.load() 
      self.compile()

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

    #self.loader.show_summary(show_images=False)

    self._end(self.load_dataset.__name__)


  # Create a sequential model
  def create(self):
    self._start(self.create.__name__)
    input_shape = self.x_train.shape[1:]
 
    print(input_shape)
    
    self.model = self.VegeFruitsAutoEncoderModel(input_shape)

    self._end(self.create.__name__)


  def compile(self):
    self._start(self.compile.__name__)
    #self.model.compile(optimizer='adam', 
    #                   loss='categorical_crossentropy', metrics = ['accuracy'])
    self.model.compile(optimizer='adadelta', loss='binary_crossentropy')
                       
    self._end(self.compile.__name__)


  def train(self):  
    self._start(self.train.__name__)
    start = time.time()
    print("Epochs " + str(self.epochs))
    print(self.x_train.shape)
    print(self.y_train.shape)

    if (self.use_checkpoint_cb == True) :
      check_point_cb = ModelCheckpoint(self.weight_filepath, 
                    monitor="acc", verbose=1,
                     save_best_only=True, save_weights_only=True)
      self.callbacks.append(check_point_cb)

    print(self.callbacks)
    
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
    self.model.summary()
    
    self._end(self.train.__name__)


  def predict(self): 
    self._start(self.predict.__name__)
    # Call self.model.predict method to get decoded_images from x_test image
    self.decoded_images = self.model.predict(self.x_test)
    self._end(self.predict.__name__)


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
      self.write("Found weight_filepath:'{}'".format(self.weight_filepath))
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
   
    dataset_id = VegeFruits_10
    
    epochs     = 20
    if len(sys.argv) ==2:
      epochs = int(sys.argv[1])
 
    print("dataset_id:{} epochs:{}".format(dataset_id, epochs))

    model = VegeFruitsAutoEncoder(dataset_id, epochs, None,
                         ipaddress="127.0.0.1", port=7777, use_checkpoint_cb=True)
    
    model.build()
    model.predict()
    model.show_images()

  except:
    traceback.print_exc()

