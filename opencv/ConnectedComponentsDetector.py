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

  class BinarizedImageView(ZOpenCVImageView):

    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)
      
    def load(self, filename):
      image = self.load_opencv_image(filename)
      self.source_image = image.copy()
      #self.gray_image = cv2.cvtColor(self.source_image, cv2.COLOR_RGB2GRAY)
      self.gray_image = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2GRAY)
             
    def binarize(self, adaptive_method_id, threshold_type_id, block_size):
      MAX_PIXEL_VALUE = 255
      C               = 9.0  
     
      self.binarizered_image = cv2.adaptiveThreshold(self.gray_image,  MAX_PIXEL_VALUE, 
          adaptive_method_id, threshold_type_id, block_size,  C);
          
      #self.set_opencv_image(binarizered_image)
      self.update()
      
    def detect_connected_components(self):
      target = self.source_image.copy()
      
      nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(self.binarizered_image, 4)  
      #stats = cv2.connectedComponentsWithStats(self.gray_image)
      print("labels:{}".format(nlabels))
      ih, iw, c = target.shape
      print("target:width={} height={} channels={}".format(iw, ih, c))
      for i in range(nlabels):         
        x, y, w, h, a = stats[i] 
        print("x,y,w,h, a={},{},{},{}, {}".format(x, y, w, h, a))
        
        cv2.rectangle(target, (x, y), (x + w, y + h), (0,0,255), 3) 
           
      self.set_opencv_image(target)
      self.update()    

  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/Shapes.png"
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.binarized_image_view = self.BinarizedImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
      
    # 4 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)
    self.add(self.binarized_image_view)

    self.show()
  

  def add_control_pane(self, fixed_width=220):
    # Control pane widget
    self.block_size = 11
    self.vpane = ZVerticalPane(self, fixed_width)

    self.adaptive_method_id = 0;
    self.threshold_type_id  = 0;
    
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
    
    self.labeled_slider = ZLabeledSlider(self.vpane, "BlockSize", take_odd =True,  
              minimum=3, maximum=43, value=self.block_size, fixed_width=200)
    self.labeled_slider.add_value_changed_callback(self.slider_value_changed)
    
    self.vpane.add(self.adaptive_method)
    self.vpane.add(self.threshold_type)    
    self.vpane.add(self.labeled_slider)

    self.set_right_dock(self.vpane)

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load(filename)
    self.binarized_image_view.load(filename)
    
    self.binarized_image_view.binarize(self.adaptive_method_id, self.threshold_type_id, self.block_size)
    self.binarized_image_view.detect_connected_components()
    self.set_filenamed_title(filename)
      
  
  def slider_value_changed(self, value):
    self.block_size = int(value)
    if self.block_size % 2 == 0:
      self.block_size = int((self.block_size * 2)/2 + 1)
      # Block size should be odd.
    print("slider_value_changed:{}".format(self.block_size))
    self.binarized_image_view.binarize(self.adaptive_method_id, self.threshold_type_id, self.block_size)
    self.binarized_image_view.detect_connected_components()
     
  def adaptive_method_activated(self, text):
    print("adaptive_method_activated:{}".format(text))
    self.adaptive_method_id = self.methods[text]
    
    self.binarized_image_view.binarize(self.adaptive_method_id, self.threshold_type_id, self.block_size)
    self.binarized_image_view.detect_connected_components()

  def threshold_type_activated(self, text):
    print("threshold_type_activated:{}".format(text))
    self.threshold_type_id = self.types[text]
    self.binarized_image_view.binarize(self.adaptive_method_id, self.threshold_type_id, self.block_size)
    self.binarized_image_view.detect_connected_components()
     
     
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

