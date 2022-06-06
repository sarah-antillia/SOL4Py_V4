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

#  ZOpenCVImageView.py
 
# 2018/05/05 Updated

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno

from SOL4Py.opencv.ZOpenCVImageConverter  import ZOpenCVImageConverter

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

class ZOpenCVImageView(QWidget):

  # Constructor
  # 2018/05/05
  # Modified to be able to take filename and flags parameters.
  def __init__(self, parent, filename=None, flags=cv2.IMREAD_COLOR):
    super(ZOpenCVImageView, self).__init__(parent)
    self.opencv_image = None
    self.rgbimage = None
    self.pixmap  = None
    # Check filename whether it's not None and is string.
    if filename != None and isinstance(filename, str):
      self.load_opencv_image(filename, flags)
    else:
      # Do nothing here. 
      pass
    
  def load_opencv_image(self, filename, flags = cv2.IMREAD_COLOR):
    if filename != None:
      abspath = os.path.abspath(filename)
      #print("abspath:{}".format(abspath))
   
      if not os.path.isfile(abspath):
        raise FileNotFoundError(errno.ENOENT, 
              os.strerror(errno.ENOENT), abspath)
     
      # OpenCV original image
      self.opencv_image = cv2.imread(abspath, flags)
      self.set_opencv_image(self.opencv_image)
      return self.opencv_image
      
    else:
      return None
   
           
  def set_opencv_image(self, cvimage):
    # Ths cvimage read by cv2.imread is BGR, so we have to convert it to a RGB format.
    # This ZOpenCVImageConvert converts a color or gray scale image to a rgb image
    image_converter = ZOpenCVImageConverter()
    
    self.rgbimage = image_converter.convert_to_rgb(cvimage)
    if self.rgbimage.all() != None:
      if len(self.rgbimage.shape) == 3:
        height, width, channels = self.rgbimage.shape
        bytesPerLine = channels * width
        qimage  = QImage(self.rgbimage.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.pixmap.size(), Qt.KeepAspectRatio)
      
      else:
        self.pixmap = None
        #raise exception

  def resize_to_image(self):
    if self.rgbimage.all() != None:
      if len(self.rgbimage.shape) == 3:
        height, width, channels = self.rgbimage.shape
        self.resize(width, height)
       
  def paintEvent(self, event):
    painter = QPainter(self)
    size    = self.size()
    point   = QPoint(0,0) 
    if self.pixmap != None:
      scaled_pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
      painter.drawPixmap(point, scaled_pixmap)
      
  def get_opencv_image(self):
    return self.opencv_image
    
  def get_qpixmap(self):
    return self.pixmap
    
