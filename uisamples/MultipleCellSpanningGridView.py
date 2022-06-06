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

 
#  MultipleCellSpanningGridView.py
 
# 2018/05/01

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno

#from PyQt5.QtWidgets import *
#from PyQt5.QtGui     import *
#from PyQt5.QtCore    import *

sys.path.append('../')

from SOL4Py.ZApplicationView     import *
from SOL4Py.ZImageView           import *
from SOL4Py.opencv.ZOpenCVImageView     import *

#---------------------------------------------------------------------
#
if __name__ == '__main__':
  applet  = QApplication(sys.argv)
  appview = QWidget()
  appview.setWindowTitle(sys.argv[0])
  grid    = QGridLayout(appview)
  image_views = [None, None, None]
  filenames   = ["../images/Pedestrian.png", "../images/Pedestrian8.png", 
                 "../images/MenInWhite2.jpg"] 
                 #"../images/flower3.jpg",
                 #"../images/flower7.jpg"]

  flags = cv2.IMREAD_COLOR
  image_views[0] = ZOpenCVImageView(appview, filenames[0], flags)
  image_views[1] = ZOpenCVImageView(appview, filenames[1], flags) 
  image_views[2] = ZOpenCVImageView(appview, filenames[2], flags)
  
  grid.addWidget(image_views[0], 0, 0)
  grid.addWidget(image_views[1], 0, 1)
  grid.addWidget(image_views[2], 1, 0, 1, 2)
      
  
  
  appview.setGeometry(40, 40, 800, 400)
  appview.show()
  
  applet.exec_()

