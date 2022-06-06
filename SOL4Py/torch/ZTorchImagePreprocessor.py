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

# ZTorchImagePreprocessor.py

# encodig: utf-8

import sys
import os
import time
import traceback
import numpy as np

import torch
import torchvision
import torchvision.transforms as transforms
from torch.autograd import Variable


class ZTorchImagePreprocessor:
  def __init__(self):
    pass

  def preprocess(self, image, resize=256, crop=224):
    normalize = transforms.Normalize(
                  mean=[0.485, 0.456, 0.406],
                  std =[0.229, 0.224, 0.225])

    preprocessor = transforms.Compose([
                 transforms.Resize(resize),
                 transforms.CenterCrop(crop),
                 transforms.ToTensor(),
                 normalize
                 ])
    return preprocessor(image)


  def image_crop(self, image, resize=256, crop=224):
    crop_preprocessor = transforms.Compose([
       transforms.Resize(resize),
       transforms.CenterCrop(crop)
    ])
    return crop_preprocessor(image)

