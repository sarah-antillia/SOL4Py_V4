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

# 2019/07/13

#  TorchRoadSignsModel.py

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

from TorchRoadSignsDataset import *

ROADSIGNS  = 0


############################################################
# Classifier Model class

class TorchRoadSignsModel(ZMLModel):
  IMAGE_SIZE = 64 # 128
  
  ##
  # Constructor
  def __init__(self, dataset_id, epochs=0, mainv=None, ipaddress="127.0.0.1", port=7777):
    super(TorchRoadSignsModel, self).__init__(0, mainv)

    
    #self.view   = mainv
    self._start(self.__init__.__name__)
    
    self.write("dataset_id:{}, ephochs:{}, mainv:{}".format(dataset_id, epochs, mainv) )
    self.ipaddress = ipaddress
    self.port      = port 
    self.model     = None   # 
    self.dataset_id = dataset_id  # ROADSIGNS
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
        self.save()

      except:
        traceback.print_exc()
    
    self._end(self.build.__name__)

  
  #
  def load_dataset(self, data_root = "./dataset/", 
                   batch_size_train= 64,
                   batch_size_test = 16, try_augmentation=False):
                   
    self._start(self.load_dataset.__name__)
    
    if try_augmentation==True:
      self.train_tranformer = transforms.Compose(
                     [
                      transforms.Resize((self.IMAGE_SIZE, self.IMAGE_SIZE)),
                      transforms.RandomCrop((self.IMAGE_SIZE-4, self.IMAGE_SIZE-4)),
                      transforms.RandomHorizontalFlip(),
                      transforms.ToTensor(),
                      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    else:
      self.train_transformer = transforms.Compose(
                     [
                      transforms.Resize((self.IMAGE_SIZE, self.IMAGE_SIZE)),
                      transforms.ToTensor(),
                      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
     
    self.valid_transformer = transforms.Compose(
                     [ 
                      transforms.Resize((self.IMAGE_SIZE, self.IMAGE_SIZE)),
                      transforms.ToTensor(),
                      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

                
    # Load ROADSIGNS
    if self.dataset_id == ROADSIGNS:
      # create train/valid datasets
      train_root = data_root + "/train/"
      self.train_dataset = TorchRoadSignsDataset(root= train_root, 
                            transform=self.train_transformer)
      valid_root = data_root + "/valid/"
      self.valid_dataset = TorchRoadSignsDataset(root= valid_root, 
                            transform=self.valid_transformer)
      self.classes  = self.train_dataset.classes
      self.nclasses = self.train_dataset.nclasses
      # create train/val loaders

      self.train_loader = DataLoader(dataset=self.train_dataset,
                                batch_size  = batch_size_train, 
                                shuffle     = True,
                                num_workers = 2)
      self.valid_loader = DataLoader(dataset=self.valid_dataset,
                              batch_size    = batch_size_test, 
                              shuffle       = False,
                              num_workers   = 2)

      
    self._end(self.load_dataset.__name__)


  # Create a sequential model
  def create(self):
    self._start(self.create.__name__)
    self.image_size = (3, self.IMAGE_SIZE, self.IMAGE_SIZE)
    
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


  def predict(self, input):
    #image_tensor = self.valid_transformer(image).float()
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

        
############################################################
#    

if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
   
    dataset_id = ROADSIGNS
    epochs     = 20 #2019/04/25
    
    if len(sys.argv) >= 2:
      dataset_id = int(sys.argv[1])
      
    if len(sys.argv) >= 3:
      epochs = int(sys.argv[2])
     
    print("dataset_id:{} epochs:{}".format(dataset_id, epochs))
    
    
    if dataset_id == ROADSIGNS:
      model = TorchRoadSignsModel(dataset_id, epochs, None)
      model.build()
    else:
      print("Invalid dataset_id: {}".format(dataset_id))

  except:
    traceback.print_exc()

