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

#  ZOpenCVImageConverter.py

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno

class ZOpenCVImageConverter:

  def __init__(self):
    pass
    
  # Convert bgr image read by cv2.imread to rgb image to paint it in 
  # PyQt5 world.
  def convert_to_rgb(self, image):
    # For simplicity, in case of gray scale, we convert it to RGB
    # This is the case of gray scale
    if len(image.shape) == 2:
      rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
      return rgb
      
    # If lenght of image.shape is 3.
    if len(image.shape) == 3:
      height, width, channels = image.shape
      rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      return rgb

