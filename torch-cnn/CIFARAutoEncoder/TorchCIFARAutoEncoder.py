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

# 2019/07/25

#  TorchCIFARTAutoEncoder.py


# On CIFAR-10 dataset, see the following page:

# http://www.cs.toronto.edu/~kriz/cifar.html

# See: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#loading-and-normalizing-cifar10


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

from SOL4Py.torch.ZTorchSimpleAutoEncoderModel import ZTorchSimpleAutoEncoderModel
from SOL4Py.torch.ZTorchEpochChangeNotifier import ZTorchEpochChangeNotifier
from SOL4Py.torch.ZTorchModelCheckPoint import ZTorchModelCheckPoint

CIFAR10  = 0
CIFAR100 = 1


##
# CIFAR AutoEncoder class

class TorchCIFARAutoEncoder(ZMLModel):

  IMAGE_SIZE = 32
  CHANNELS   = 3 
   
  ##
  # Constructor
  def __init__(self, dataset_id, epochs=0, mainv=None, ipaddress="127.0.0.1", port= 8888):
    super(TorchCIFARAutoEncoder, self).__init__(dataset_id, mainv)
    self.write("====================================")
    self._start(self.__init__.__name__)

    self.model_filepath   = None

    self.set_input_shape()
    self.nclasses = 10

    self.epochs   = epochs
    self.batch_size = 128
    notifier = self.__class__.__name__+str("-") + str(self.dataset_id)
    print("epochs {}".format(self.epochs))
    
    self.callbacks = [ZTorchEpochChangeNotifier(ipaddress, port, notifier, int(self.epochs)+10),
                      ZTorchModelCheckPoint(dataset_id=dataset_id)]

    self.model_filename  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".pt"
    self.write(self.model_filename)

    # Set training and validation transformer
    self.create_image_transformer()
    self._end(self.__init__.__name__)


  # Define your own create_image_transformer method derived from this class if required.
  def create_image_transformer(self):
    self.train_transformer = transforms.Compose(
                     [transforms.ToTensor()] )
     
    self.valid_transformer = transforms.Compose(
                     [transforms.ToTensor()] )


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


  def set_input_shape(self):
    self.input_shape = (self.IMAGE_SIZE, self.IMAGE_SIZE, 1)


  def set_dataset_id(self, dataset_id):
    self.dataset_id = dataset_id
    self.model_filename  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".pt"
    #self.model = None


  #
  def load_dataset(self, data_root = "./data", 
                   batch_size_train= 128,
                   batch_size_test = 64):
                   
    self._start(self.load_dataset.__name__)


    # Load CIFAR10
    if self.dataset_id == CIFAR10:
      self.trainset = torchvision.datasets.CIFAR10(
               root=data_root, train=True, download=True, transform=self.train_transformer)
               
      self.train_loader = torch.utils.data.DataLoader(
               self.trainset, batch_size=batch_size_train, shuffle=True, num_workers=2)

      self.validset = torchvision.datasets.CIFAR10(
               root=data_root, train=False, download=True, transform=self.valid_transformer)

      self.valid_loader = torch.utils.data.DataLoader(
               self.validset, batch_size=batch_size_test, shuffle=False, num_workers=2)
      self.nclasses = 10

    # Load CIFAR100
    if self.dataset_id == CIFAR100:
      self.trainset = torchvision.datasets.CIFAR100(
               root=data_root, train=True, download=True, transform=self.train_transformer)
               
      self.train_loader = torch.utils.data.DataLoader(
               self.trainset, batch_size=batch_size_train, shuffle=True, num_workers=2)

      self.validset = torchvision.datasets.CIFAR100(
               root=data_root, train=False, download=True, transform=self.valid_transformer)

      self.valid_loader = torch.utils.data.DataLoader(
               self.validset, batch_size=batch_size_test, shuffle=False, num_workers=2)

      self.nclasses = 100
      
    self._end(self.load_dataset.__name__)


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


  # Remove model file and weight file.
  def clear(self):
    if self.trained():
      os.remove(self.model_filename)
      self.model = None


  def is_trained(self):
    self._start(self.trained.__name__)
    rc = False
  
    if os.path.isfile(self.model_filename) == True:
      self.write("Found model file:'{}'".format(self.model_filename))
      rc = True
    self._end(self.trained.__name__)
    
    return rc


  def predict(self, dataset_loader, n_sampling=10):
    # Call self.model.predict method to get decoded_images from data_loader
    return self.model.predict(dataset_loader, n_sampling=n_sampling)


  def show_images(self, dataset_loader, decoded_images, n_sampling=10):
    self.model.show_images(dataset_loader, decoded_images,  n_sampling)


  def save(self):
    self._start(self.save.__name__)
    self.model.save()
    self._end(self.save.__name__)


  def load(self):
    self._start(self.load.__name__)
    self.model.load_model()        
    self._end(self.load.__name__)



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

    model = TorchCIFARAutoEncoder(dataset_id=dataset_id, epochs=epochs)
    model.build()
    
    sampling = 10
    decoded_images = model.predict(model.valid_loader,    n_sampling=sampling)
    
    model.show_images(model.valid_loader, decoded_images, n_sampling=sampling)
    
  except:
    traceback.print_exc()

