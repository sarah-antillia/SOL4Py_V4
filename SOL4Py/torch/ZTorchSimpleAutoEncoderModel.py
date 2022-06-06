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

# ZTorchSimpleAutoEncoderModel.py

# See: https://github.com/L1aoXingyu/pytorch-beginner/tree/master/08-AutoEncoder
# See also: https://github.com/L1aoXingyu/pytorch-beginner/blob/master/08-AutoEncoder/conv_autoencoder.py

# encodig: utf-8

import sys
import os
import time
import traceback

import matplotlib.pyplot as plt
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
#conda install tqdm
from collections import OrderedDict 

sys.path.append('../')

from SOL4Py.torch.ZTorchModel    import ZTorchModel
from SOL4Py.torch.ZTorchEpochChangeNotifier    import ZTorchEpochChangeNotifier
from SOL4Py.torch.ZTorchModelCheckPoint    import ZTorchModelCheckPoint


class ZTorchSimpleAutoEncoderModel(ZTorchModel):
  #
  # Constructor
  def __init__(self, image_size, n_classes, model_filename):
    super(ZTorchSimpleAutoEncoderModel, self).__init__(image_size, n_classes, model_filename)
    self.n_classes      = n_classes
    self.image_size     = image_size;
    ch, h, w            = image_size
    
    print("ch:{} h:{} w:{}".format(ch, h, w))    
    self.model_filename = model_filename
    
    self.encoder = None
    self.decoder = None
    self.ch      = ch
    self.size    = h

    self.create_encoder()
    self.create_decoder()

    print("{}".format(self))


  # Convlutional encoder
  def create_encoder(self):    
    self.encoder = nn.Sequential(
        nn.Conv2d(3, 12,  4, stride=2, padding=1), 
        nn.ReLU(),
        nn.Conv2d(12, 24, 4, stride=2, padding=1),
        nn.ReLU(),
        nn.Conv2d(24, 48, 4, stride=2, padding=1),
        nn.ReLU(),
    )

  def create_decoder(self):
    self.decoder = nn.Sequential(
        nn.ConvTranspose2d(48, 24, 4, stride=2, padding=1),
        nn.ReLU(),
        nn.ConvTranspose2d(24, 12, 4, stride=2, padding=1),
        nn.ReLU(),
        nn.ConvTranspose2d(12,  3, 4, stride=2, padding=1),
        nn.Sigmoid(),
       )


  def encode(self, x):
    return self.encoder(x)


  def decode(self, x):
    return self.decoder(x)


  def forward(self, input_image):
    encoded = self.encode(input_image)
    decoded = self.decode(encoded)
    return decoded 


  def fit(self, train_loader, 
                valid_loader, 
                callbacks,
                epochs,
                criterion, 
                optimizer):

    self.epochs = epochs 
    self.callbacks = callbacks

    self.train_loader = train_loader
    self.valid_loader = valid_loader

    if criterion == None:    
      criterion = nn.MSELoss()
    if optimizer == None:
      optimizer = torch.optim.Adam(self.parameters(),
                             lr=0.01,
                             weight_decay=1e-5)

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
        train_loss, val_loss = 0, 0
        
        # Change the net model to a training mode.
        net.train()

        for i, (images, labels) in enumerate(pbar):
          ch, h, w = images[0].size()
          if ch == 1:
            images = images.view(images.size(0), -1)
               
          images = images.to(device)
          images = Variable(images)
          
          optimizer.zero_grad()
          
          outputs = net(images)
          loss = criterion(outputs, images)
          train_loss += loss.item()

          loss.backward()

          optimizer.step()
          pbar.set_postfix(OrderedDict(
                epoch="{:>10}".format(epoch),
                loss ="{:.4f}".format(loss.item())))

        avg_train_loss = train_loss / len(self.train_loader.dataset)
        
        # Change the net model to a validation mode. 
        net.eval()
        print("Validating epoch {}".format(epoch))
    
        with torch.no_grad():
          for images, labels in self.valid_loader:
            ch, h, w = images[0].size()
            if ch == 1:
              images = images.view(images.size(0), -1)


            images = images.to(device)
            images = Variable(images)

            outputs = net(images)
            loss = criterion(outputs, images)
            val_loss += loss.item()

        avg_val_loss = val_loss / len(self.valid_loader.dataset)

        logs = { 
                "loss"     : avg_train_loss, 
                "val_loss" : avg_val_loss, }

        print("logs : {}".format(logs))
        for callback in self.callbacks:
          if  type(callback) == ZTorchEpochChangeNotifier or type(callback) == ZTorchModelCheckPoint:
            callback.on_epoch_end(epoch, logs)


  # This method can be used encode and decode images through dataset_loader.
  # Returns decoded_image_list 
  def predict(self,  
                dataset_loader,
                n_sampling = 10, 
                criterion  = None):

    self.dataset_loader  = dataset_loader
    if criterion == None:    
      criterion = nn.MSELoss()

    device = self.get_device()

    net = self.to(device)

    # Change net model to validation mode 
    net.eval()

    images_list = []

    ### Start an evaluation by using the valid_loader.
    val_loss = 0.0

    with torch.no_grad():
      samples = 0
      for images, labels in self.dataset_loader:
        if samples == n_sampling:
          break
        else:
          samples = samples + 1

        ch, h, w = images[0].size()
        if ch == 1:
          # Gray scale image
          images = images.view(images.size(0), -1)
  
        images = images.to(device)
        images = Variable(images)

        outputs = net(images)
        
        images_list.append(outputs[0])
        
        loss = criterion(outputs, images)
        val_loss += loss.item()

    avg_val_loss = val_loss / len(self.dataset_loader.dataset)

    logs = {"val_loss" : avg_val_loss, }

    print("logs : {}".format(logs))
      
    return images_list  

  # Read images from dataset_loader and decoded_images, and show them on plt.
  def show_images(self, dataset_loader, decoded_images, n_sampling):
    
    it = iter(dataset_loader)
    n = n_sampling
    
    fig = plt.figure(figsize=(n * 2, 4))
    for i in range(1, n + 1):
        images, labels = it.next()

        # Display original x_test images
        ax = plt.subplot(2, n, i)
        npimage = images[0].numpy()
        #ch, h, w = npimage.shape

        npimage = np.transpose(npimage, (1, 2, 0))
        plt.imshow(npimage)

        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Display decoded images predicted from original images. 
        ax = plt.subplot(2, n, i + n)

        npimage = decoded_images[i-1].numpy()
        npimage = np.transpose(npimage, (1, 2, 0))
          
        plt.imshow(npimage)

        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    fig.tight_layout()
    plt.show()


