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

#  ScrolledImageViewer.py

# encodig: utf-8

import sys
import os
import traceback

#from PyQt5.QtCore    import *
#from PyQt5.QtWidgets import *
#from PyQt5.QtGui     import *

sys.path.append('../')

from SOL4Py.ZLabeledComboBox     import *
from SOL4Py.ZLabeledSlider       import *
from SOL4Py.ZApplicationView     import *
from SOL4Py.opencv.ZOpenCVScrolledImageView     import ZOpenCVScrolledImageView
 
class MainView(ZApplicationView):

  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
       
    filename = "../images/MenInWhite2.jpg"
    
    # 1 Create an imageview in the main_widget 
    self.image_view = ZOpenCVScrolledImageView(self)
    
    # 2 Load opencv image into the imageview.
    self.image_view.load_opencv_image(filename)

    # 3 Add the imageview to the main_layout
    self.add(self.image_view)

    self.set_filenamed_title(filename)
    
    self.show()
       
  # Default file_open method to read an image file by using ZOpenCVImageReader
  # and set the image read to the first area of ZDrawingArea.
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.image_view.load_opencv_image(filename)
      self.set_filenamed_title(filename)
      
####
if main(__name__):
  try:
    name   = os.path.basename(sys.argv[0])
    applet = QApplication(sys.argv)
        
    mainv  = MainView(name, 40, 40, 640,300)
    mainv.show ()

    applet.exec_()

  except:
    traceback.print_exc()

