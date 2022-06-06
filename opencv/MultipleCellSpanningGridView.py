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
# 2018/05/05

# encodig: utf-8

import sys
import os
import cv2
import traceback


from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

# 
sys.path.append('../')

from SOL4Py.ZApplicationView import *
from SOL4Py.ZLabeledComboBox import ZLabeledComboBox
from SOL4Py.ZLabeledSlider   import ZLabeledSlider
from SOL4Py.opencv.ZOpenCVImageView import ZOpenCVImageView  
from SOL4Py.ZVerticalPane    import ZVerticalPane 
from SOL4Py.ZGridLayouter    import ZGridLayouter 
 
class MainView(ZApplicationView):
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    grid = ZGridLayouter(self)
    
    image_views = [None, None, None]
    filenames   = ["../images/Pedestrian.png", 
                   "../images/Pedestrian8.png", 
                   "../images/MenInWhite2.jpg"] 
 
    flags = cv2.IMREAD_COLOR
    image_views[0] = ZOpenCVImageView(grid, filenames[0], flags)
    image_views[1] = ZOpenCVImageView(grid, filenames[1], flags) 
    image_views[2] = ZOpenCVImageView(grid, filenames[2], flags)
  
    grid.add(image_views[0], 0, 0)
    grid.add(image_views[1], 0, 1)
    grid.add(image_views[2], 1, 0, 1, 2)
    
    self.show()
  
  
#*************************************************
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 900, 380)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

