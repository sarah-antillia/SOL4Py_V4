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

#  HomogeneousBlur.py

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
      self.load_openv_image(filename)
      self.update()

  class BlurredImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)
      
    def load(self, filename):
      self.load_openv_image(filename)
      
    def blur(self, ksize):
      ksize = int(ksize)
      original_image = self.get_opencv_image()
      blurred_image = cv2.blur(original_image,  
                    (ksize, ksize))
                     
      self.set_opencv_image(blurred_image)
      self.update()
      
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/flower.png"
    
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

  
  # Add control pane to MainView
  def add_control_pane(self, fixed_width=200):
    # Control pane widget
    self.ksize = 11
    self.vpane = ZVerticalPane(self, fixed_width)
    
    self.labeled_slider = ZLabeledSlider(self.vpane, "KernelSize", take_odd =True,  
              minimum=0, maximum=33, value=self.ksize)
    
    self.labeled_slider.add_value_changed_callback(self.slider_value_changed)
    
    self.vpane.add(self.labeled_slider)

    self.set_right_dock(self.vpane)

  # Show FileOpenDialog and select an image file.
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load_opencv_image(filename,  cv2.IMREAD_COLOR)
    self.blurred_image_view.load_opencv_image(filename, cv2.IMREAD_COLOR)
    self.blurred_image_view.blur(int(self.ksize))
    self.set_filenamed_title(filename)
      
  # Slider value changed callback.
  def slider_value_changed(self, value):
    self.ksize = int(value)
    if self.ksize % 2 == 0:
      self.ksize = (self.ksize * 2)/2 + 1
      # Kernel size should be odd.
    #print("slider_value_changed:{}".format(ksize))
    self.blurred_image_view.blur(int(int(self.ksize)))
     
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

