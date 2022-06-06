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

# 2019/06/28
# See: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#loading-and-normalizing-cifar10

#  TorchCIFARModel.py

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
 
sys.path.append('../../')

from SOL4Py.ZMain import *
from SOL4Py.ZMLModel import *

from SOL4Py.torch.ZTorchEpochChangeNotifier import *
from SOL4Py.torch.ZTorchSimpleModel      import *

CIFAR10  = 0
CIFAR100 = 1


############################################################
# Classifier Model class

class TorchCIFARModel(ZMLModel):
  ##
  # Constructor
  def __init__(self, dataset_id, epochs=0, mainv=None, ipaddress="127.0.0.1", port=7777):
    super(TorchCIFARModel, self).__init__(0, mainv)

    #self.view   = mainv
    self._start(self.__init__.__name__)
    
    self.write("dataset_id:{}, ephochs:{}, mainv:{}".format(dataset_id, epochs, mainv) )
    self.ipaddress = ipaddress
    self.port      = port 
    self.model     = None   # 
    self.dataset_id = dataset_id  # CIFAR10 or CIFAR100
    self.dataset   = None
    self.epochs    = epochs
    self.set_dataset_id(dataset_id)
  
    notifier = self.__class__.__name__+str("-") + str(self.dataset_id)

    self.callbacks = [ZTorchEpochChangeNotifier(ipaddress, port, notifier, int(self.epochs)+10)]

    self._end(self.__init__.__name__)


  def set_dataset_id(self, dataset_id):
    self._start(self.set_dataset_id.__name__)
    self.dataset_id   = dataset_id
    
    self.model_filename  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".pt"
    
    self.nclasses     = 0
    self.write("model_filename  " + self.model_filename)

    self._end(self.set_dataset_id.__name__)


  def build(self):
    self.write("====================================")
    self._start(self.build.__name__)
    
    if self.is_trained() != True:
      try:
        self.load_dataset()
        self.create()
      
        self.train()
        #self.evaluate()
        self.save()

      except:
        traceback.print_exc()
    
    self._end(self.build.__name__)

  
  #
  def load_dataset(self, data_root = "./data", 
                   batch_size_train= 128,
                   batch_size_test = 64):
                   
    self._start(self.load_dataset.__name__)
    
    self.train_transformer = transforms.Compose(
                     [transforms.ToTensor(),
                      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
     
    self.test_transformer = transforms.Compose(
                     [transforms.ToTensor(),
                      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    # Load CIFAR10
    if self.dataset_id == CIFAR10:
      self.trainset = torchvision.datasets.CIFAR10(
               root=data_root, train=True, download=True, transform=self.train_transformer)
               
      self.train_loader = torch.utils.data.DataLoader(
               self.trainset, batch_size=batch_size_train, shuffle=True, num_workers=2)

      self.testset = torchvision.datasets.CIFAR10(
               root=data_root, train=False, download=True, transform=self.test_transformer)

      self.test_loader = torch.utils.data.DataLoader(
               self.testset, batch_size=batch_size_test, shuffle=False, num_workers=2)

      self.nclasses = 10

 
    # Load CIFAR100
    if self.dataset_id == CIFAR100:
      self.trainset = torchvision.datasets.CIFAR100(
               root=data_root, train=True, download=True, transform=self.train_transformer)
               
      self.train_loader = torch.utils.data.DataLoader(
               self.trainset, batch_size=batch_size_train, shuffle=True, num_workers=2)

      self.testset = torchvision.datasets.CIFAR100(
               root=data_root, train=False, download=True, transform=self.test_transformer)

      self.test_loader = torch.utils.data.DataLoader(
               self.testset, batch_size=batch_size_test, shuffle=False, num_workers=2)


      self.nclasses = 100
      
    self._end(self.load_dataset.__name__)


  # Create a sequential model
  def create(self):
    self._start(self.create.__name__)
    self.image_size = (3, 32, 32)
    
    print("classes {}".format(self.nclasses))
    self.model = ZTorchSimpleModel(self.image_size, self.nclasses, self.model_filename)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    self.model = self.model.to(device)

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


  def predict(self, input):
    #image_tensor = self.test_transformer(image).float()
    #image_tensor = image_tensor.unsqueeze_(0)
    #input = Variable(image_tensor)

    prediction = self.model.predict(input)
     
    return prediction
 

  def save(self):
    self._start(self.save.__name__)
    self.model.save()
    self._end(self.save.__name__)
      

  def load(self):
    self._start(self.load.__name__)
  
    try:                
      self.model.load_model()
      #self.write("Loaded a weight file:{}".format(self.model_file))

    except:
      self.write( formatted_traceback() )

    self._end(self.load.__name__)


  def get_model(self):
    return self.model


  def is_trained(self):
    rc = False
    
    if os.path.isfile(self.model_filename) == True:
      self.write("Found model_filename:'{}'".format(self.model_filename))
      rc = True
    return rc


  def evaluate(self):
    self._start(self.evaluate.__name__)
    try:
      score = 0 # self.model.evaluate(self.X_test, self.y_test, verbose=0)
      #self.write("Test loss    :{}".format(score[0]))     
      #self.write("Test accuracy:{}".format(score[1]))
      pass
    except:
      self.write(formatted_traceback())
      
    self._end(self.evaluate.__name__)


        
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
      model = TorchCIFARModel(dataset_id, epochs, None)
      model.build()
    else:
      print("Invalid dataset_id: {}".format(dataset_id))

  except:
    traceback.print_exc()

