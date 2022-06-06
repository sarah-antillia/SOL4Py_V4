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

#  CIFARDenosingAutoEncoderModel.py

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


#sys.path.append('../../')

#from SOL4Py.ZMLModel import *
#from SOL4Py.ZMain    import *

#from SOL4Py.keras.ZEpochChangeNotifier import *
#from SOL4Py.keras.ZSimpleAutoEncoderModel import *

sys.path.append('../')
from CIFARAutoEncoder.CIFARAutoEncoder import *

# Define CIFARDenosingAutoEncoder derived from CIFARAutoEncoder,
# because there are quite similar interfaces between them, 
# to load_data_set, to create  a model, to compile, to train and 
# to predict methods, apart from the input_data to be noise-injected or not.


class CIFARDenoisingAutoEncoder(CIFARAutoEncoder):

  ##
  # Constructor
  def __init__(self, dataset_id = CIFAR10, 
                     epochs=20, mainv=None, ipaddress="127.0.0.1", port=8888):

    super(CIFARDenoisingAutoEncoder, self).__init__(dataset_id, epochs, mainv, ipaddress, port)


  # Weight file will be created in the current_dir, so you should define
  # set_weigth_filename method in each model class.
  # Build a full path name to a weight_file name from self.__class_.__name__ and currend_dir.
  def set_weight_filepath(self):
    weight_file = self.__class__.__name__ + "_"  + str(self.dataset_id) + ".h5" 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    self.weight_filepath = os.path.join(current_dir, weight_file)
    print("self.weight_filepath:{}".format(self.weight_filepath))


  # Override supepr().load_dataset method to inject noise to the original x_train and x_test data. 
  def load_dataset(self):
    super().load_dataset()
   
    # Inject noise to the orginal dataset self.x_train and self.x_test.
    self.x_train = self.inject_noise_into(self.x_train)
    self.x_test  = self.inject_noise_into(self.x_test )


  # Redefine your own noise injection method if required.
  # See: https://keras.io/examples/mnist_denoising_autoencoder/
  def inject_noise_into(self, data):
    # Make Gaussian noise by using np.random.normal of size=data.shape
    noise = np.random.normal(loc=0.5, scale=0.5, size=data.shape)
    noised = data + noise
    return np.clip(noised, 0.0, 1.0)



#################################################
#
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
   
    epochs     = 20
    if len(sys.argv) ==2:
      epochs = int(sys.argv[1])

    model = CIFARDenoisingAutoEncoder(dataset_id= 0, 
                                  epochs= epochs)
    model.build()
    
    model.predict()
    model.show_images()
    
  except:
    traceback.print_exc()

