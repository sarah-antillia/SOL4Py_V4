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

# 2019/07/23

#  ZPILSaultPepperNoise.py

# encodig: utf-8

import sys
import os
import time
import traceback
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps, ImageFilter

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision.transforms as transforms
from torch.utils.data import DataLoader

from SOL4Py.ZSaultPepperNoiseInjector import *


class ZPILSaultPepprerNoise(object):
  ##
  # Constructor
  def __init__(self, sigma):
    # Create an object ZGaussianNoiseInjector
    self.noise_injector = ZGaussianNoiseInjector(sigma=sigma)

  def __call__(self, image):
    arrayed_image = np.asarray(image)
    noised_image = self.noise_injector.inject_to(arrayed_image)

    # Create a PIL image from the noised_image
    return Image.fromarray(noised_image)

