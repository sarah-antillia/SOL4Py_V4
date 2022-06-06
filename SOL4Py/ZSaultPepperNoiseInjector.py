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

#  ZSaultPepperNoiseInjector.py

# encoding: utf-8

import sys
import os
import numpy as np

import traceback

from SOL4Py.ZNoiseInjector import *

class ZSaultPepperNoiseInjector(ZNoiseInjector):

  ##
  #
  # Constructor
  def __init__(self, sault=0.05, pepper=0.05):
    self.sault  = sault
    self.pepper = pepper

  def inject_to(self, image):
    src_image = image.astype(np.float32)
    # 1 Create a zero-filled image from the src_image. 
    noised_image = np.zeros(image.shape, np.float32)

    for i in range(image.shape[0]): 
     for j in range(image.shape[1]): 
      r = np.random.random() 
      if r < self.sault: 
       noised_image[i][j] = 0.0 
      elif r > 1.0 - self.pepper: 
       noised_image[i][j] = 255.0 
      else: 
       noised_image[i][j] = image[i][j] 

    noised_image = np.clip(noised_image, 0.0, 255.0)
    noised_image = noised_image.astype(np.uint8)

    return noised_image

