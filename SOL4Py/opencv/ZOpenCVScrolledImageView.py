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

#  ZOpenCVScrolledImageView.py
 
# 2018/05/05 Updated

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno


from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from SOL4Py.opencv.ZOpenCVImageView       import *

class ZOpenCVScrolledImageView(QScrollArea):

  def __init__(self, parent, filename=None, flags=cv2.IMREAD_COLOR):
    super(ZOpenCVScrolledImageView, self).__init__(parent)
    self.image_view = ZOpenCVImageView(parent, filename, flags)
    self.image_view.load_opencv_image(filename, flags)
    
    self.setWidget(self.image_view)
    
  def load_opencv_image(self, filename, flags = cv2.IMREAD_COLOR):    
    image = self.image_view.load_opencv_image(filename, flags)
    if image.all() != None:
      self.image_view.resize_to_image()
  

  def set_opencv_image(self, cvimage):
    self.image_view.set_opencv_image(cvimage)
      
  def get_opencv_image(self):
    return self.image_view.get_opencv_image()
    
  def get_qpixmap(self):
    return self.image_view.get_qpixmap()
    
  def get_image_view(self):
    return self.image_view
    
