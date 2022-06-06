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

#  ZGaussianNoiseInjector.py

# encoding: utf-8

import sys
import os
import numpy as np

import traceback

from SOL4Py.ZNoiseInjector import *

class ZGaussianNoiseInjector(ZNoiseInjector):
  ##
  # Constructor
  def __init__(self, sigma=40):
    self.sigma = sigma

  def inject_to(self, image):
    src_image = image.astype(np.float32)
    # 1 Create a zero-filled image from the src_image. 
    noised_image = np.zeros(image.shape, np.float32)

    # 2 Create a one channel noise.
    noise = np.random.randn(image.shape[0], image.shape[1]) * self.sigma
    noise = noise.astype(np.float32)

    # 3 Add the noise to the source image.
    if len(noised_image.shape) == 2: # Grayscale 
      noised_image = image + noise
    else:
      noised_image[:,:, 0] = image[:,:, 0] + noise
      noised_image[:,:, 1] = image[:,:, 1] + noise
      noised_image[:,:, 2] = image[:,:, 2] + noise

    noised_image = np.clip(noised_image, 0.0, 255.0)
    noised_image = noised_image.astype(np.uint8)

    return noised_image

