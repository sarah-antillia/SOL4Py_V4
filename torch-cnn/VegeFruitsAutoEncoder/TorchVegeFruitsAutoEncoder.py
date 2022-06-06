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

# 2019/07/20

#  TorchVegeFruitsTAutoEncoder.py


# encodig: utf-8

import sys
import os
import time
import traceback

import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
from torch.autograd import Variable

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision.transforms as transforms
from torch.utils.data import DataLoader

sys.path.append('../../')


from SOL4Py.ZMLModel import *
from SOL4Py.ZMain    import *
#from SOL4Py.ZGaussianNoise import ZGaussianNoise

from SOL4Py.torch.ZTorchSimpleAutoEncoderModel import ZTorchSimpleAutoEncoderModel
from SOL4Py.torch.ZTorchEpochChangeNotifier import ZTorchEpochChangeNotifier
from SOL4Py.torch.ZTorchModelCheckPoint import ZTorchModelCheckPoint

sys.path.append('../')

#from VegeFruits.TorchVegeFruitsDataset import TorchVegeFruitsDataset
from VegeFruits.TorchVegeFruitsModel import TorchVegeFruitsModel

VegeFruits  = 0


############################################################
# VegeFruits AutoEncoder class

class TorchVegeFruitsAutoEncoder(TorchVegeFruitsModel):

  IMAGE_SIZE = 64
  CHANNELS   = 3 
   
  ##
  # Constructor
  def __init__(self, dataset_id, epochs=0, mainv=None, ipaddress="127.0.0.1", port= 8888):
    super(TorchVegeFruitsAutoEncoder, self).__init__(dataset_id, epochs, mainv, ipaddress, port)
    
    self.create_image_transformer()


  # Define your own create_image_transformer method in a subclass derived from this class if required.
  def create_image_transformer(self):
    self.train_transformer = transforms.Compose(
                     [
                      transforms.Resize((self.IMAGE_SIZE, self.IMAGE_SIZE)),
                      transforms.ToTensor()] )
     
    self.valid_transformer = transforms.Compose(
                     [ 
                      transforms.Resize((self.IMAGE_SIZE, self.IMAGE_SIZE)),
                      transforms.ToTensor() ] )

    self._end(self.__init__.__name__)



  def build(self):
    self._start(self.build.__name__)
    try:
      self.load_dataset()
      self.create()

      if self.is_trained() ==False:
        self.train()
        self.save()
      else:
        self.load()
 
    except:
      traceback.print_exc()

    self._end(self.build.__name__)


  def create(self):
    self._start(self.create.__name__)
    self.image_size = (self.CHANNELS, self.IMAGE_SIZE, self.IMAGE_SIZE)
    self.model_filename  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".pt"

    self.model = ZTorchSimpleAutoEncoderModel(self.image_size,  self.nclasses, self.model_filename )
                 
    self._end(self.create.__name__)


  def train(self):  
    self._start(self.train.__name__)
    start = time.time()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(self.model.parameters(),lr=0.01, weight_decay=1e-5)
    
    self.model.fit(self.train_loader,
                   self.valid_loader,
                   self.callbacks,
                   self.epochs,
                   criterion, 
    	           optimizer)

    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self.model.summary()
    self._end(self.train.__name__)


  def predict(self, dataset_loader, n_sampling=10):
    # Call self.model.predict method to get decoded_images from data_loader
    return self.model.predict(dataset_loader, n_sampling=n_sampling)


  def show_images(self, dataset_loader, decoded_images, n_sampling=10):
    self.model.show_images(dataset_loader, decoded_images, n_sampling)


############################################################
#
#

if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])
    dataset_id = 0
    
    epochs     = 10
    if len(sys.argv) >= 2:
      dataset_id = int(sys.argv[1])

    if len(sys.argv) == 3:
      epochs = int(sys.argv[2])

    model = TorchVegeFruitsAutoEncoder(dataset_id=dataset_id, epochs=epochs)
    model.build()
    
    sampling = 10
    decoded_images = model.predict(model.valid_loader,    n_sampling=sampling)
 
    model.show_images(model.valid_loader, decoded_images, n_sampling=sampling)
    
  except:
    traceback.print_exc()

