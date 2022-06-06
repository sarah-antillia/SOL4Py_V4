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

#  TorchMNISTAutoEncoder.py

# This is based on the following sample program.
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
#  https://www.kaggle.com/tinydman/fashion-mnist-with-pytorch

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
from torchvision.datasets import MNIST, FashionMNIST

sys.path.append('../../')


from SOL4Py.ZMLModel import *
from SOL4Py.ZMain    import *

from SOL4Py.torch.ZTorchSimpleAutoEncoderModel import ZTorchSimpleAutoEncoderModel
from SOL4Py.torch.ZTorchEpochChangeNotifier import ZTorchEpochChangeNotifier
from SOL4Py.torch.ZTorchModelCheckPoint import ZTorchModelCheckPoint

MNIST         = 0
FASHION_MNIST = 1


############################################################
# Classifier Model clas

class TorchMNISTAutoEncoderModel(ZTorchSimpleAutoEncoderModel):
  ##
  # Constructor
  def __init__(self, image_size, n_classes, model_filename):
    super(TorchMNISTAutoEncoderModel, self).__init__(image_size, n_classes, model_filename)
    pass

  def create_encoder(self):    
    self.encoder = nn.Sequential(
      nn.Linear(self.size * self.size, 128),
      nn.ReLU(True),
      nn.Linear(128, 64),
      nn.ReLU(True),
      nn.Linear(64, 12),
      nn.ReLU(True),
      nn.Linear(12, 2))


  def create_decoder(self):
    self.decoder = nn.Sequential(
        nn.Linear(2, 12),
        nn.ReLU(True),
        nn.Linear(12, 64),
        nn.ReLU(True),
        nn.Linear(64, 128),
        nn.ReLU(True),
        nn.Linear(128, self.size * self.size),
        nn.Tanh()
    )


       
class TorchMNISTAutoEncoder(ZMLModel):
  IMAGE_SIZE = 28
  CHANNELS   = 1    #1: Gray scale
   
  ##
  # Constructor
  def __init__(self, dataset_id, epochs=0, mainv=None, ipaddress="127.0.0.1", port= 8888):
    super(TorchMNISTAutoEncoder, self).__init__(dataset_id, mainv)
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
    
    # Create training and validation transformer.
    self.create_image_transformer()
        
    self._end(self.__init__.__name__)
 

  # Define your own create_image_transformer method in a subclass derived from this class if required.
  def create_image_transformer(self):
    self.train_transformer = transforms.Compose([transforms.ToTensor()])
    self.valid_transformer = transforms.Compose([transforms.ToTensor()])


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


  def load_dataset(self):
    self._start(self.load_dataset.__name__)
    
    if self.dataset_id == MNIST:
      self.train_data = torchvision.datasets.MNIST("./data", train=True, download=True, transform=self.train_transformer)
      self.train_loader = torch.utils.data.DataLoader(self.train_data,
                         batch_size=self.batch_size,
                         shuffle=True)
                         
      self.test_data   = torchvision.datasets.MNIST("./data", train=False, download=True, transform=self.valid_transformer)
      self.valid_loader = torch.utils.data.DataLoader(self.test_data,
                         batch_size=self.batch_size,
                         shuffle=False)      
    if self.dataset_id == FASHION_MNIST:
      self.train_data = torchvision.datasets.FashionMNIST("./data", train=True, download=True, transform=self.train_transformer)
      self.train_loader = torch.utils.data.DataLoader(self.train_data,
                         batch_size=self.batch_size,
                         shuffle=True)
                         
      self.test_data   = torchvision.datasets.FashionMNIST("./data", train=False, download=True, transform=self.valid_transformer)
      self.valid_loader = torch.utils.data.DataLoader(self.test_data,
                         batch_size=self.batch_size,
                         shuffle=False)      

    self._end(self.load_dataset.__name__)


  def create(self):
    self._start(self.create.__name__)
    self.image_size = (1, self.IMAGE_SIZE, self.IMAGE_SIZE)
    self.model_filename  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".pt"

    self.model = TorchMNISTAutoEncoderModel(self.image_size,  self.nclasses, self.model_filename )
    
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
    # Call self.model.predict method to get decoded_images from x_test image
    return self.model.predict(dataset_loader, n_sampling=n_sampling)


  def show_images(self, dataset_loader, decoded_images,  n_sampling=10):    
    it = iter(dataset_loader)
    n = n_sampling
    fig = plt.figure(figsize=(n * 2, 4))
    for i in range(1, n + 1):
        images, labels = it.next()

        # Display original x_test images
        ax = plt.subplot(2, n, i)
        npimage = images[0].numpy()
        ch, h, w = npimage.shape
        #print("src", npimage.shape)
        plt.imshow(npimage.reshape(h, w))

        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Display decoded images predicted from original images. 
        ax = plt.subplot(2, n, i + n)
        npimage = decoded_images[i-1].numpy()
        #print("dec", npimage.shape)
        
        plt.imshow(npimage.reshape(h, w))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    fig.tight_layout()
    plt.show()


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

    model = TorchMNISTAutoEncoder(dataset_id=dataset_id, epochs=epochs)
    model.build()

    sampling = 10
    decoded_images = model.predict(model.valid_loader,    n_sampling=sampling)
    
    model.show_images(model.valid_loader, decoded_images, n_sampling=sampling)
    
  except:
    traceback.print_exc()

