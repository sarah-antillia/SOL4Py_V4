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

# 2019/06/25

# ZTorchModule.py

# This is a simple subclass to inherit torch cnn.Module
# This will be used as a base class, for example,
#  AlexNet: https://github.com/icpm/pytorch-cifar10/blob/master/models/AlexNet.py
# See: https://github.com/vinhkhuc/PyTorch-Mini-Tutorials/blob/master/5_convolutional_net.py

# encodig: utf-8

import sys
import os
import time
import traceback
import numpy as np

import torch
import torchvision
import torch.nn as nn
import torch.nn.init as init
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.autograd import Variable

from tqdm import tqdm
# Please install tqdm to display a progress bar by using conad commad 
# conda install tqdm

from collections import OrderedDict 

sys.path.append('../')
from SOL4Py.torch.ZTorchEpochChangeNotifier import ZTorchEpochChangeNotifier
from SOL4Py.torch.ZTorchModelCheckPoint    import ZTorchModelCheckPoint


## 
# ZTorchModel

class ZTorchModel(nn.Module):
  #
  # Constructor
  # Please define your own Constructor in a subclass derived from this class
  def __init__(self, image_size, n_classes, model_filename):
    super(ZTorchModel, self).__init__()
    self.n_classes      = n_classes
    self.image_size     = image_size;
    
    ch, h, w            = image_size
    print("ch:{} h:{} w:{}".format(ch, h, w))    
    self.model_filename = model_filename


  # Please define your own forward method in a subclass derived from this class
  def forward(self, input):
    return input


  def show_model_state(self):
    for param in self.state_dict():
      print(param, "\t", model.state_dict()[param].size())


  # This method may be used without any modification in a subclass derived from this class.
  # Sorry, this is a very ugly implementation, far from elegant.
  # We have been using tqdm to display a progress bar in a console window(command line prompt).

  def fit(self, train_loader, 
                test_loader, 
                callbacks,
                epochs,
                criterion, 
                optimizer):

    self.epochs = epochs 
    self.callbacks = callbacks

    self.train_loader = train_loader
    self.test_loader  = test_loader
    
    if criterion == None:    
      criterion = nn.CrossEntropyLoss()
    if optimizer == None:
      optimizer = optim.SGD(self.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)
    
    device = self.get_device()
    net = self.to(device)
      
    ### Start training
    for callback in self.callbacks:
      if type(callback) == ZTorchEpochChangeNotifier:
        logs = {"epochs": epochs}
        callback.on_train_begin(logs)

    for epoch in range(self.epochs):
      
      print("Training epoch:{}".format(epoch))

      with tqdm(self.train_loader, ncols=100) as pbar:
        train_loss, train_acc, val_loss, val_acc = 0, 0, 0, 0
        
        # Change the net model to a training mode.
        net.train()

        for i, (images, labels) in enumerate(pbar):
          images = images.to(device)
          labels = labels.to(device)
          optimizer.zero_grad()
          outputs = net(images)
          loss = criterion(outputs, labels)
          train_loss += loss.item()
          train_acc  += (outputs.max(1)[1] == labels).sum().item()

          loss.backward()

          optimizer.step()
          pbar.set_postfix(OrderedDict(
                epoch="{:>10}".format(epoch),
                loss ="{:.4f}".format(loss.item())))

        avg_train_loss = train_loss / len(self.train_loader.dataset)
        avg_train_acc  = train_acc  / len(self.train_loader.dataset)
        
        # Change the net model to a validation mode. 
        net.eval()
        print("Validating epoch {}".format(epoch))
    
        with torch.no_grad():
          for images, labels in self.test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = net(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            val_acc  += (outputs.max(1)[1] == labels).sum().item()

        avg_val_loss = val_loss / len(self.test_loader.dataset)
        avg_val_acc  = val_acc  / len(self.test_loader.dataset)

        logs = {"acc"      : avg_train_acc, 
                "loss"     : avg_train_loss, 
                "val_acc"  : avg_val_acc,
                "val_loss" : avg_val_loss, }

        print("logs : {}".format(logs))
        for callback in self.callbacks:
          if  type(callback) == ZTorchEpochChangeNotifier or type(callback) == ZTorchModelCheckPoint:
            callback.on_epoch_end(epoch, logs)


  # This method may be used without any modification in a subclass derived from this class
  def evalute(self,  
                test_loader, 
                criterion,
                epochs):
                
    self.epochs = epochs 

    self.test_loader  = test_loader
    
    device = self.get_device()
    net = self.to(device)
    
    # Change net model to validation mode 
    net.eval()
      
    ### Start an evaluation by using the test_loader.
    
    for epoch in range(self.epochs):
      print("Validating epoch {}".format(epoch))
      val_loss, val_acc = 0, 0

      with torch.no_grad():
        for images, labels in self.test_loader:
          images = images.to(device)
          labels = labels.to(device)
          outputs = net(images)
          loss = criterion(outputs, labels)
          val_loss += loss.item()
          val_acc  += (outputs.max(1)[1] == labels).sum().item()

      avg_val_loss = val_loss / len(self.test_loader.dataset)
      avg_val_acc  = val_acc  / len(self.test_loader.dataset)

      logs = {"val_acc"  : avg_val_acc,
              "val_loss" : avg_val_loss, }

      print("logs : {}".format(logs))



  def save(self):
    torch.save(self.state_dict(), self.model_filename)
    print("Saved model parameters to " + self.model_filename)

  def get_device(self):
    return "cuda" if torch.cuda.is_available() else "cpu"


  def predict(self, input):
    device = self.get_device()

    input = input.to(device)
    output = self(input)
    index = output.data.cpu().numpy().argmax()
    #print("predict index: {}".format(index))
    
    return index


  def is_trained(self):
    rc = False
    if os.path.exists(self.model_filename):
      rc = True
    return rc


  def load_model(self):
    if os.path.isfile(self.model_filename):
      # Load trained model parameters file.
      dic = torch.load(self.model_filename)
      self.load_state_dict(dic)
      print("Loaded model file {}.".format(self.model_filename))
    else:
      raise Exception("Not found file:" + self.model_filename)


  def summary(self):
    #, input_size):
    #input_size will take a tuple(ch, h, w)
    #summary(self, input_size=input_size)
    print(self)
    
