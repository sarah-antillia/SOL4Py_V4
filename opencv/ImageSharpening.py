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

#  ImageSharpening.py

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


class MainView(ZApplicationView):
  # Inner classes
  #--------------------------------------------
  class SourceImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)

    def load(self, filename):
      self.load_opencv_image(filename)
      self.update()

  class SharpenedImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)
      
    def load(self, filename):
      self.load_opencv_image(filename)
       
    def sharpen(self, ksize, sigma):
      source_image = self.get_opencv_image()
      blurred = cv2.GaussianBlur(source_image, (ksize, ksize), 
            float(sigma), #sigmaX, 
            float(sigma), #sigmaY
            cv2.BORDER_DEFAULT)

      alpha = 2.5
      beta  = 1.0 - alpha
      sharpened = cv2.addWeighted(source_image, alpha, blurred, beta, 0.0)
      
      self.set_opencv_image(sharpened)
   
      self.update()
      
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/Cloud.png"
        
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.sharpened_image_view = self.SharpenedImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
    
    # 4 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)
    self.add(self.sharpened_image_view)

    self.show()
  

  def add_control_pane(self, fixed_width=200):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)
     
    self.ksize    =  21
    self.sigmaSize = 12
    
    self.ksize_slider = ZLabeledSlider(self.vpane, "KernelSize", take_odd =True,  
              minimum=0, maximum=31, value=self.ksize)    
    self.ksize_slider.add_value_changed_callback(self.slider1_value_changed)
    self.vpane.add(self.ksize_slider)

    self.sigmaSize_slider = ZLabeledSlider(self.vpane, "SigmaSize", take_odd =False,  
              minimum=0, maximum=30, value=self.sigmaSize)    
    self.sigmaSize_slider.add_value_changed_callback(self.slider2_value_changed)
    self.vpane.add(self.sigmaSize_slider)
    

    self.set_right_dock(self.vpane)

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load  (filename)
    self.sharpened_image_view.load(filename)
    
    # Apply sharpen method to the sharpened image view.
    self.sharpened_image_view.sharpen(self.ksize, self.sigmaSize)
    
    self.set_filenamed_title(filename)
 
  
  def slider1_value_changed(self, value):
    self.ksize = int(value)
    self.sharpened_image_view.sharpen(int(self.ksize), int(self.sigmaSize))

  def slider2_value_changed(self, value):
    self.sigmaSize = int(value)
    self.sharpened_image_view.sharpen(int(self.ksize), int(self.sigmaSize))
     
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

