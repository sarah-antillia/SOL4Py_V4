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

#  BilateralFilter.py

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

  class BlurredImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)
      
    def load(self, filename):
      source_image = self.load_opencv_image(filename)
      self.gray_image = cv2.cvtColor(source_image, cv2.COLOR_RGB2GRAY)
             
    def blur(self, diameter, sigma_color, sigma_space):
      source_image = self.get_opencv_image()
      print("blur {} {} {}".format(diameter, sigma_color, sigma_space))
      blurred_image = cv2.bilateralFilter(source_image, diameter, 
            float(sigma_color),  
            float(sigma_space) ) 
            
      self.set_opencv_image(blurred_image)
      self.update()
      
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/MeshedNioh.png"
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.blurred_image_view = self.BlurredImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
      
    # 4 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)
    self.add(self.blurred_image_view)

    self.show()
  

  def add_control_pane(self, fixed_width=220):
    # Control pane widget

    self.vpane = ZVerticalPane(self, fixed_width)
    
    self.diameter     = 4
    self.sigma_color  = 160
    self.sigma_space  = 40
        
    self.diameter_slider = ZLabeledSlider(self.vpane, "Diameter", take_odd =False,  
              minimum=0, maximum=5, value=self.diameter, fixed_width=200)
    self.diameter_slider.add_value_changed_callback(self.diameter_value_changed)


    self.sigma_color_slider = ZLabeledSlider(self.vpane, "SigmaColor", take_odd =False,  
              minimum=0, maximum=255, value=self.sigma_color, fixed_width=200)
    self.sigma_color_slider.add_value_changed_callback(self.sigma_color_value_changed)
    
    self.sigma_space_slider = ZLabeledSlider(self.vpane, "SigmaSpace", take_odd =False,  
              minimum=0, maximum=255, value=self.sigma_space, fixed_width=200)
    self.sigma_space_slider.add_value_changed_callback(self.sigma_space_value_changed)
    
    self.vpane.add(self.diameter_slider)
    self.vpane.add(self.sigma_color_slider)
    self.vpane.add(self.sigma_space_slider)
    
    self.set_right_dock(self.vpane)

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load(filename)
    self.blurred_image_view.load(filename)
    
    self.blurred_image_view.blur(self.diameter, self.sigma_color, self.sigma_space)

    self.set_filenamed_title(filename)
      
  
  def diameter_value_changed(self, value):
    self.diameter= int(value)
    self.blurred_image_view.blur(self.diameter, self.sigma_color, self.sigma_space)
     
  def sigma_color_value_changed(self, value):
    self.sigma_color = int(value)
    self.blurred_image_view.blur(self.diameter, self.sigma_color, self.sigma_space)

  def sigma_space_value_changed(self, value):
    self.sigma_space = int(value)
    self.blurred_image_view.blur(self.diameter, self.sigma_color, self.sigma_space)


     
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

