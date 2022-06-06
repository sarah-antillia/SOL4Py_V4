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

#  GridLayoutOpenCVImageView.py
 
# 2018/05/01

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

sys.path.append('../')

from SOL4Py.ZImageView           import ZImageView
from SOL4Py.opencv.ZOpenCVImageView     import ZOpenCVImageView

#---------------------------------------------------------------------
#
if __name__ == '__main__':
  applet  = QApplication(sys.argv)
  appview = QWidget()
  appview.setWindowTitle(sys.argv[0])
  grid    = QGridLayout(appview)
  image_views = [None, None, None, None, None, None]
  filenames   = ["../images/flower.png", "../images/flower1.jpg", 
                 "../images/flower2.jpg", "../images/flower3.jpg",
                 "../images/flower7.jpg"]

  for i in range(len(filenames)):  
    image_views[i] = ZOpenCVImageView(appview) #, 0, 0, 400, 300)
    image_views[i].load_opencv_image(filenames[i], i % 3)
    y = int(i % 3)
    x = int(i / 3)
    
    grid.addWidget(image_views[i], x, y)
  
  appview.setGeometry(40, 40, 800, 400)
  appview.show()
  
  applet.exec_()

