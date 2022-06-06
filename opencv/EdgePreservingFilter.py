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

 
class MainView(ZApplicationView):
  # Inner classes
  #--------------------------------------------
  class SourceImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)

    def load(self, filename):
      self.load_opencv_image(filename)
      self.update()

  class FilteredImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)
      
    def load(self, filename):
      self.source_image= self.load_opencv_image(filename)
      
    def filter(self, sigmaColor, sigmaSpace):
      
      if self.source_image.all() != None:
        flag = cv2.RECURS_FILTER

        filtered_image = cv2.edgePreservingFilter(
            self.source_image,  
            flag,
            sigma_s = sigmaSpace, 
            sigma_r = float(sigmaColor)/100.0)
            
        self.set_opencv_image(filtered_image)
        self.update()
      
  #--------------------------------------------
  

  SIGMA_COLOR_MAX = 100;
  SIGMA_SPACE_MAX = 200;
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/flower.png"
        
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.filtered_image_view = self.FilteredImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
    
    # 4 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)
    self.add(self.filtered_image_view)

    self.show()
  

  def add_control_pane(self, fixed_width=200):
    self.vbox = QWidget(self)
    self.vbox.setMinimumWidth(fixed_width)
    self.vbox.setMaximumWidth(fixed_width)
     
    vlayout = QVBoxLayout(self.vbox)
    self.sigmaColor =  40
    self.sigmaSpace =  160
    
    self.sigmaColor_slider = ZLabeledSlider(self.vbox, "SigmaColor", take_odd =False,  
              minimum=0, maximum=self.SIGMA_COLOR_MAX, value=self.sigmaColor)    
    self.sigmaColor_slider.add_value_changed_callback(self.slider1_value_changed)
    vlayout.addWidget(self.sigmaColor_slider)

    self.sigmaSpace_slider = ZLabeledSlider(self.vbox, "SigmaSpace", take_odd =False,  
              minimum=0, maximum=self.SIGMA_SPACE_MAX, value=self.sigmaSpace)    
    self.sigmaSpace_slider.add_value_changed_callback(self.slider2_value_changed)
    
    vlayout.addWidget(self.sigmaSpace_slider)
    
    vlayout.setAlignment(Qt.AlignTop)

    self.set_right_dock(self.vbox)

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load  (filename)
    self.filtered_image_view.load(filename)
    
    # Apply filter method to the filtered image view.
    self.filtered_image_view.filter(self.sigmaColor, self.sigmaSpace)
    self.set_filenamed_title(filename)
      
  
  def slider1_value_changed(self, value):
    self.sigmaColor = int(value)
    #print("SigmaColor:{}".format(self.sigmaColor))
    self.filtered_image_view.filter(int(self.sigmaColor), int(self.sigmaSpace))

  def slider2_value_changed(self, value):
    self.sigmaSpace = int(value)
    #print("SigmaSpace:{}".format(self.sigmaSpace))
    self.filtered_image_view.filter(int(self.sigmaColor), int(self.sigmaSpace))
     
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
     pass

