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

# 2018/09/05 Updated.

#  ZImageView.py

# encodig: utf-8

import sys
import os
import traceback
import numpy as np
import qimage2ndarray

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

#---------------------------------------------------------------------

class ZImageView(QWidget):

  def __init__(self, parent, x, y, width, height, keepAspectRatio=True):
    super(ZImageView, self).__init__(parent)
    self.pixmap = None
    self.keepAspectRatio = keepAspectRatio    
    self.setGeometry(x, y, width, height)
    self.scale = 1.0
    self.pixmap_size = None
    self.gray_color_table = [qRgb(i, i, i) for i in range(256)]
    

  def load_image(self, filename):
    self.pixmap  = QPixmap(filename) # 
    self.pixmap = self.pixmap.scaled(self.pixmap.size(), Qt.KeepAspectRatio)
    self.pixmap_size = self.pixmap.size()
    
    #2018/09/04 Modified to change the size of this imageview to fit the size of self.pixmap.
    size = self.pixmap.size()
    size = size * float(self.scale)
    self.setGeometry(0, 0, size.width(), size.height())
    self.repaint()


  def paintEvent(self, event):
    painter = QPainter(self)
    
    if self.pixmap != None:
      size  = self.pixmap.size() 
      # This is really identical to self.pixmap.size(), because we fitted the sizeof widget 
      #to the size of self.pixmap in load_image method.
      
      point = QPoint(0, 0) 
      
      # 2018/09/10 Added the following line
      size = size * float(self.scale)
 
      if self.keepAspectRatio == True:
        scaled_pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, 
                 transformMode = Qt.SmoothTransformation)
        painter.drawPixmap(point, scaled_pixmap)
      else:
        painter.drawPixmap(point, self.pixmap)


  def get_pixmap(self):
    return self.pixmap

    
  def set_image(self, ndarray):
    # https://pypi.org/project/qimage2ndarray/
    qimage = qimage2ndarray.array2qimage(ndarray)
                  
    self.pixmap =QPixmap.fromImage(qimage)
    self.pixmap_size = self.pixmap.size()
    size = self.pixmap.size()
    size = size * float(self.scale)
    self.setGeometry(0, 0, size.width(), size.height())
    self.repaint()
    
  def rescale(self, percentage):
    self.scale = float(percentage)/100.0
    # 2019/05/15
    if self.pixmap !=None:
      size = self.pixmap.size() 
      size = size * float(self.scale)
      self.setGeometry(0, 0, size.width(), size.height())

    self.repaint()


  def file_save(self, filepath):
    _, ext = os.path.splitext(filepath)
    print("file_save ", ext)
    
    ext = ext.replace(".", "")
 
    self.pixmap.save(filepath, ext)
    
