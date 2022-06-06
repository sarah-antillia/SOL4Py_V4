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

#  TripleImageView.py

# encodig: utf-8

import sys
import os
import cv2
import traceback

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.opencv.ZOpenCVImageView  import ZOpenCVImageView  
 

class MainView(ZApplicationView):

  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
    
    self.image_views = [None, None, None]
    
    filenames = ["../images/flower.png", 
                 "../images/flower5.jpg", 
                 "../images/flower7.jpg"]
    flags     = [cv2.IMREAD_COLOR, 
                 cv2.IMREAD_GRAYSCALE, 
                 cv2.IMREAD_UNCHANGED]

    # Get the main horizontal layout from the parent ZApplicationView.    

    # Create imageviews, load images from the filenames, and add those imageviews to the main layout.
    for i in range(len(self.image_views)) :
      self.image_views[i] = ZOpenCVImageView(self)
      self.image_views[i].load_opencv_image(filenames[i], flags[i] )
      self.add(self.image_views[i])

    self.show()
    
####
    
if main(__name__):
  try:
    name   = os.path.basename(sys.argv[0])
    applet = QApplication(sys.argv)
  
    main_view  = MainView(name, 40, 40, 900, 380)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

