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

#  OpenCVImageView.py
 
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

from SOL4Py.opencv.ZOpenCVImageView           import ZOpenCVImageView

#---------------------------------------------------------------------
# Unit test
#
if __name__ == '__main__':
  try:
    applet = QApplication(sys.argv)
    image_view = ZOpenCVImageView(parent=None)
  
    image_view.load_opencv_image("../images/flower.png", cv2.IMREAD_GRAYSCALE)
    image_view.setGeometry(40, 40, 400, 300)
    image_view.show()
  
    applet.exec_()
  
  except:
    traceback.print_exc()
