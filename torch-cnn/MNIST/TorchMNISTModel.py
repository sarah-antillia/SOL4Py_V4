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

# 2019/07/03

#  MNISTModel.py

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

from SOL4Py.torch.ZTorchMNISTModel import ZTorchMNISTModel
from SOL4Py.torch.ZTorchEpochChangeNotifier import ZTorchEpochChangeNotifier
from SOL4Py.torch.ZTorchModelCheckPoint import ZTorchModelCheckPoint

MNIST         = 0
FASHION_MNIST = 1


############################################################
# Classifier Model clas

class TorchMNISTModel(ZMLModel):
        
  ##
  # Constructor
  def __init__(self, dataset_id, epochs=0, mainv=None, ipaddress="127.0.0.1", port=7777):
    super(TorchMNISTModel, self).__init__(dataset_id, mainv)
    self.write("====================================")
    self._start(self.__init__.__name__)

    self.model_filepath   = None

    self.image_rows = 28 
    self.image_cols = 28
    
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
    
    self._end(self.__init__.__name__)
 
 
  def build(self):
    self._start(self.build.__name__)
    try:
      self.load_dataset()
      self.create()
              
      if self.is_trained() ==False:
        self.train()
        self.save()

      self.evaluate()

    except:
      traceback.print_exc()

    self._end(self.build.__name__)


  def set_input_shape(self):
    self.input_shape = (self.image_rows, self.image_cols, 1)


  def set_dataset_id(self, dataset_id):
    self.dataset_id = dataset_id
    self.model_filename  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".pt"
    #self.model = None



  def load_dataset(self):
    self._start(self.load_dataset.__name__)
    
    self.transformer = transforms.Compose([transforms.ToTensor()])
                                #transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    if self.dataset_id == MNIST:
      self.train_data = torchvision.datasets.MNIST("./data", train=True, download=True, transform=self.transformer)
      self.train_loader = torch.utils.data.DataLoader(self.train_data,
                         batch_size=self.batch_size,
                         shuffle=True)
                         
      self.test_data   = torchvision.datasets.MNIST("./data", train=False, download=True, transform=self.transformer)
      self.test_loader = torch.utils.data.DataLoader(self.test_data,
                         batch_size=self.batch_size,
                         shuffle=False)      
    if self.dataset_id == FASHION_MNIST:
      self.train_data = torchvision.datasets.FashionMNIST("./data", train=True, download=True, transform=self.transformer)
      self.train_loader = torch.utils.data.DataLoader(self.train_data,
                         batch_size=self.batch_size,
                         shuffle=True)
                         
      self.test_data   = torchvision.datasets.FashionMNIST("./data", train=False, download=True, transform=self.transformer)
      self.test_loader = torch.utils.data.DataLoader(self.test_data,
                         batch_size=self.batch_size,
                         shuffle=False)      
 

    self._end(self.load_dataset.__name__)


  def create(self):
    self._start(self.create.__name__)
    self.image_size = (1, self.image_rows, self.image_cols)
    self.model_filename  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".pt"

    self.model = ZTorchMNISTModel(self.image_size,  self.nclasses, self.model_filename )
    self._end(self.create.__name__)


  def train(self):  
    self._start(self.train.__name__)
    start = time.time()
    criterion = nn.CrossEntropyLoss()
    
    optimizer = optim.SGD(self.model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)
    
    self.model.fit(self.train_loader,
                   self.test_loader,
                   self.callbacks,
                   self.epochs,
                   criterion, 
    	           optimizer)


    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self.model.summary()
    self._end(self.train.__name__)


  def evaluate(self):
    self._start(self.evaluate.__name__)
    criterion = nn.CrossEntropyLoss()

    self.model.evalute(self.test_loader,
                    criterion,
                    self.epochs)
    self._end(self.evaluate.__name__)
     

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


  def save(self):
    self._start(self.save.__name__)
    self.model.save()
    self._end(self.save.__name__)


  def load(self):
    self._start(self.load.__name__)
    self.model.load_model()        
    self._end(self.load.__name__)


  def predict(self, image):

    image_tensor = self.transformer(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input = Variable(image_tensor)

    prediction = self.model.predict(input)
     
    return prediction


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
      model = TorchMNISTModel(dataset_id, epochs, None)
      model.build()
    else:
      print("Invalid dataset_id: {}".format(dataset_id))

  except:
    traceback.print_exc()

    
    