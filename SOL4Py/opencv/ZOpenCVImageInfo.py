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

#  ZOpenCVImageInfo.py

# encodig: utf-8

import numpy as np
import cv2

from SOL4Py.opengl.ZOpenGLImageInfo import *


class ZOpenCVImageInfo:
  
  def __init__(self):
    pass
    
  # Returns ZOpenGLImageInfo from the cv2.Mat image.
  def getImageInfo(self, image, flip = False, convert_to_rgb=False):
  
    bgr = image;
 
    if len(image.shape) == 3:
      height, width, channels = image.shape[:3]
    else:
      height, width = image.shape[:2]
      channels = 1
 
    if channels == 1:
      # if image is grayscale, we convert  to bgra 
      bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR);

    #dtype     = image.dtype.bytes
    if flip == True:
      bgr = cv2.flip(bgr, 0)

    if convert_to_rgb == True:
      rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    else:
      rgb = bgr

    imageInfo = ZOpenGLImageInfo()
 
    imageInfo.depth    = channels * 8; #dtype ; 
    imageInfo.channels = channels;
    imageInfo.width    = width;
    imageInfo.height   = height;
    imageInfo.format   = GL_RGB
     
    imageInfo.imageSize = rgb.nbytes  # width * height * 4; #sizeof(uint32); //Image byte size
    imageInfo.imageData = rgb;

    return imageInfo
    
