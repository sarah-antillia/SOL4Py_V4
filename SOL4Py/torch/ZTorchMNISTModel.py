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

# 2019/07/10

# ZTorchMNISTModel.py

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

sys.path.append('../')
from SOL4Py.torch.ZTorchModel    import *

## 
# ZTorchMNISTModel

class ZTorchMNISTModel(ZTorchModel):
  #
  # Constructor
  def __init__(self, image_size, n_classes, model_filename):
    super(ZTorchMNISTModel, self).__init__(image_size, n_classes, model_filename)
    ch, h, w = image_size
    #MNIST images size will be (1, 28, 28)
    print("ch:{} h:{} w:{}".format(ch, h, w))
 
    n_channels = 32
 
    self.features = nn.Sequential(
        nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1),
        nn.ReLU(inplace=True),

        nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, padding=1),
        nn.ReLU(inplace=True),

        nn.MaxPool2d(kernel_size=2, stride=1),
        nn.BatchNorm2d(16),
    
        nn.Conv2d(in_channels=16, out_channels=n_channels, kernel_size=3, padding=1),
        nn.ReLU(inplace=True),

        nn.Conv2d(in_channels=n_channels, out_channels=n_channels, kernel_size=3, padding=1),
        nn.ReLU(inplace=True),

        nn.MaxPool2d(kernel_size=2, stride=1), 
        nn.BatchNorm2d(32)
        )

    self.n_features= n_channels * (h-2) * (h-2)

    self.classifiers = nn.Sequential(
        nn.Linear(in_features=self.n_features, out_features=512),
        nn.ReLU(),
        nn.Dropout(),
        nn.Linear(in_features=512, out_features=n_classes)
        )


  def forward(self, input):
    output = self.features(input)
    output = output.view(output.size(0), self.n_features)
    output = self.classifiers(output)
    return output

