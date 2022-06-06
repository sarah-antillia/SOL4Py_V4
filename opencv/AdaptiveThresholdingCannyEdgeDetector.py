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

#  AdaptiveThresholdCannyEdgeDetector.py

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

  class DetectedImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)
      
    def load(self, filename):
      source_image = self.load_opencv_image(filename)
      self.gray_image = cv2.cvtColor(source_image, cv2.COLOR_RGB2GRAY)

    def detect(self, adaptive_method_id, threshold_type_id, block_size, threshold1, threshold2):
      MAX_PIXEL_VALUE = 255;
      C               = 9.0;  
    
      adapted_image = cv2.adaptiveThreshold(self.gray_image,  MAX_PIXEL_VALUE, 
          adaptive_method_id, threshold_type_id, block_size,  C);
      
      detected_image = cv2.Canny(adapted_image, threshold1, threshold2);
      
      self.set_opencv_image(detected_image)
      self.update()
      
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/SuperCar2.png"
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.detected_image_view = self.DetectedImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
         
    # 4 Add imageviews to the main_layout which is a horizontal layouter.
    self.add(self.source_image_view)
    self.add(self.detected_image_view)

    self.detected_image_view.detect(self.adaptive_method_id, self.threshold_type_id, self.block_size, 
                                             self.threshold1, self.threshold2)

    self.show()
  

  def add_control_pane(self, fixed_width=220):
    # Control pane widget
    self.block_size = 11
    self.vpane = ZVerticalPane(self, fixed_width)

    self.adaptive_method_id = 0
    self.threshold_type_id  = 0
    
    self.methods = {"ADAPTIVE_THRESH_MEAN_C": cv2.ADAPTIVE_THRESH_MEAN_C, 
                    "ADAPTIVE_THRESH_GAUSSIAN_C": cv2.ADAPTIVE_THRESH_GAUSSIAN_C}
    
    self.types   = {"THRESH_BINARY":  cv2.THRESH_BINARY  , 
                    "THRESH_BINARY_INV": cv2.THRESH_BINARY_INV }
    
    self.adaptive_method = ZLabeledComboBox(self.vpane, "AdaptiveMethod")
    self.adaptive_method.add_items(list(self.methods.keys() ))
    self.adaptive_method.add_activated_callback(self.adaptive_method_activated)
    
    self.threshold_type  = ZLabeledComboBox(self.vpane, "ThresholdType")
    self.threshold_type.add_items(list(self.types.keys()) )
    self.threshold_type.add_activated_callback(self.threshold_type_activated)
    
    self.block_size_slider = ZLabeledSlider(self.vpane, "BlockSize", take_odd =True,  
              minimum=3, maximum=43, value=self.block_size, fixed_width=200)
    self.block_size_slider.add_value_changed_callback(self.block_size_changed)
    self.vpane.add(self.adaptive_method)
    self.vpane.add(self.threshold_type)    
    self.vpane.add(self.block_size_slider)

    self.threshold1 =  50
    self.threshold2 = 100
    
    self.threshold1_slider = ZLabeledSlider(self.vpane, "Threshold1", take_odd =True,  
              minimum=0, maximum=300, value=self.threshold1)    
    self.threshold1_slider.add_value_changed_callback(self.slider1_value_changed)

    self.threshold2_slider = ZLabeledSlider(self.vpane, "Threshold2", take_odd =True,  
              minimum=0, maximum=300, value=self.threshold2)    
    self.threshold2_slider.add_value_changed_callback(self.slider2_value_changed)

    self.vpane.add(self.threshold1_slider)
    self.vpane.add(self.threshold2_slider)
    
    self.set_right_dock(self.vpane)

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load(filename)
    self.detected_image_view.load(filename)
    self.detected_image_view.detect(self.adaptive_method_id, self.threshold_type_id, self.block_size, 
                                             self.threshold1, self.threshold2)
    self.set_filenamed_title(filename)
      
  
  def block_size_changed(self, value):
    self.block_size = int(value)
    if self.block_size % 2 == 0:
      # Block size should be odd.
      self.block_size = int((self.block_size * 2)/2 + 1)
    #print("block_size_changed:{}".format(block_size))
    self.detected_image_view.detect(self.adaptive_method_id, self.threshold_type_id, self.block_size, 
                                             self.threshold1, self.threshold2)

  def adaptive_method_activated(self, text):
    self.adaptive_method_id = self.methods[text]
    #print("adaptive_method_activated:{}{}".format(text, self.adaptive_method_id))    
    self.detected_image_view.detect(self.adaptive_method_id, self.threshold_type_id, self.block_size, 
                                             self.threshold1, self.threshold2)
     
  def threshold_type_activated(self, text):
    self.threshold_type_id = self.types[text]
    #print("threshold_type_activated:{}{}".format(text, self.threshold_type_id))    
    self.detected_image_view.detect(self.adaptive_method_id, self.threshold_type_id, self.block_size, 
                                             self.threshold1, self.threshold2)
     
  def slider1_value_changed(self, value):
    self.threshold1 = int(value)
    #print("slider1_value_changed:{}".format(value))
    self.detected_image_view.detect(self.adaptive_method_id, self.threshold_type_id, self.block_size, 
                                             self.threshold1, self.threshold2)

  def slider2_value_changed(self, value):
    self.threshold2 = int(value)
    #print("slider2_value_changed:{}".format(value))
    self.detected_image_view.detect(self.adaptive_method_id, self.threshold_type_id, self.block_size, 
                                             self.threshold1, self.threshold2)
     
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

