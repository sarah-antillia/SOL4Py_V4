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

# 2019/04/30 

#  ZSuperResolutionSequentialModel.py
# See: https://arxiv.org/pdf/1501.00092.pdf
#      https://software.intel.com/en-us/articles/an-example-of-a-convolutional-neural-network-for-image-super-resolution

# encodig: utf-8
import os
import sys

import keras

from keras.models import Sequential
from keras.layers import *


class ZSuperResolutionSequentialModel(keras.models.Sequential):
  ##
  # Constructor
  def __init__(self, input_shape):
    super(ZSuperResolutionSequentialModel, self).__init__()

    # Create a sequential model, and add keras.layers.* to the model
    self.add(Conv2D(filters=64, kernel_size=(9, 9), padding = 'same', input_shape = input_shape))
    self.add(Activation('relu'))
    
    self.add(Conv2D(filer=32,  kernel_size=(1, 1),  padding = 'same'))
    self.add(Activation('relu'))

    self.add(Conv2D(filter=3,  kernel_size=(5, 5),  padding = 'same'))
    self.add(Activation('relu'))


  
