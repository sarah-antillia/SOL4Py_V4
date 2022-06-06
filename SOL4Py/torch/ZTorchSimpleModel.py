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
# 2019/07/13 Updated __init__ constructor to be able for w/h take 64.

# ZTorchSimpleModel.py

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
#conda install tqdm
from collections import OrderedDict 

sys.path.append('../')

from SOL4Py.torch.ZTorchModel    import ZTorchModel
from SOL4Py.torch.ZTorchEpochChangeNotifier    import ZTorchEpochChangeNotifier
from SOL4Py.torch.ZTorchModelCheckPoint    import ZTorchModelCheckPoint


## 
# ZTorchSimpleModel

class ZTorchSimpleModel(ZTorchModel):
  #
  # Constructor
  def __init__(self, image_size, n_classes, model_filename):
    super(ZTorchSimpleModel, self).__init__(image_size, n_classes, model_filename)
    self.n_classes      = n_classes
    self.image_size     = image_size;
    ch, h, w            = image_size
    print("ch:{} h:{} w:{}".format(ch, h, w))    
    self.model_filename = model_filename
 
    # The following is based on AlexNet 
    self.features = nn.Sequential(
        
        nn.Conv2d(ch, 64, kernel_size=3, padding=1),
        nn.ReLU(inplace=True),
        nn.MaxPool2d(kernel_size=2, stride=2),
        
        nn.Conv2d(64, 192, kernel_size=5, padding=2),
        nn.ReLU(inplace=True),
        nn.MaxPool2d(kernel_size=2, stride=2),
        
        nn.Conv2d(192, 384, kernel_size=3, padding=1),
        nn.ReLU(inplace=True),

        #nn.Conv2d(384, 256, kernel_size=3, padding=1),
        nn.Conv2d(384, h, kernel_size=3, padding=1),

        nn.ReLU(inplace=True),
        
        nn.Conv2d(h, h, kernel_size=3, padding=1),
        nn.ReLU(inplace=True),
        nn.MaxPool2d(kernel_size=2, stride=2),
        )

    self.n_features = 256 * 4 * 4
    
    if h == 32:
      self.n_features = h * 4 * 4  # 512
    if h == 64:
      self.n_features = h * 8 * 8  # 4096
    
    if h == 96:
      self.n_features = h * 9216   # 884736  

    if h == 128:
      self.n_features = h * h * h  #  2097152

    self.classifier = nn.Sequential(
        nn.Dropout(),
        nn.Linear(self.n_features, self.n_features),

        nn.ReLU(inplace=True),
        nn.Dropout(),
        nn.Linear(self.n_features, self.n_features),
        nn.ReLU(inplace=True),
        nn.Linear(self.n_features, n_classes)
        )


  def forward(self, input):
    output = self.features(input)
    output = output.view(output.size(0), self.n_features)
    output = self.classifier(output)
    return output




