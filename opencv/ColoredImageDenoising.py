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

#  ColoredImageDenoising.py

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
      self.load_opencv_image(filename)
      self.update()
      
    def detect(self, hParameter, hColorParameter, template_window_size, search_window_size):
      src_image = self.get_opencv_image()
      denoized_image = cv2.fastNlMeansDenoisingColored(src_image, 
          hParameter, 
          hColorParameter,
          template_window_size, search_window_size)    
      
      self.set_opencv_image(denoized_image)
      self.update()
      
  #--------------------------------------------

  # Class variables
  H_PARAMETER_MAX          = 31
  HCOLOR_PARAMETER_MAX     = 31
  TEMPLATE_WINDOW_SIZE_MAX = 31
  SEARCH_WINDOW_SIZE_MAX   = 31
        
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/MeshedNioh.png"
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.detected_image_view = self.DetectedImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
      
    
    # 4 Add imageviews to the main_layout which is a horizontal layouter.
    self.add(self.source_image_view)
    self.add(self.detected_image_view)

    self.detected_image_view.detect(self.hParameter, self.hColorParameter, 
            self.template_window_size, self.search_window_size)

    self.show()
  

  def add_control_pane(self, fixed_width=220):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)

    self.hParameter        = 21
    self.hParameter_slider = ZLabeledSlider(self.vpane, "H Parameter", take_odd =False,  
                        minimum=1, maximum=self.H_PARAMETER_MAX, value=self.hParameter)
    self.hParameter_slider.add_value_changed_callback(self.hParameter_changed)

    self.hColorParameter        = 27
    self.hColorParameter_slider = ZLabeledSlider(self.vpane, "H ColorParameter", take_odd =False,  
                        minimum=1, maximum=self.HCOLOR_PARAMETER_MAX, value=self.hColorParameter)
    self.hColorParameter_slider.add_value_changed_callback(self.hColorParameter_changed)

    self.template_window_size        = 15
    self.template_window_size_slider = ZLabeledSlider(self.vpane, "TemplateWindowSize", take_odd =False,  
                        minimum=1, maximum=self.TEMPLATE_WINDOW_SIZE_MAX, value=self.template_window_size)
    self.template_window_size_slider.add_value_changed_callback(self.template_window_size_changed)

    self.search_window_size        = 13
    self.search_window_size_slider = ZLabeledSlider(self.vpane, "SearchWindowSize", take_odd =False,  
                        minimum=1, maximum=self.SEARCH_WINDOW_SIZE_MAX, value=self.search_window_size)
    self.search_window_size_slider.add_value_changed_callback(self.search_window_size_changed)

    self.vpane.add(self.hParameter_slider)
    self.vpane.add(self.hColorParameter_slider)
    self.vpane.add(self.template_window_size_slider)
    self.vpane.add(self.search_window_size_slider)
    

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
    self.detected_image_view.detect(self.hParameter, self.hColorParameter, 
           self.template_window_size, self.search_window_size)
    self.set_filenamed_title(filename)
      
  
  def hParameter_changed(self, value):
    self.hParameter = int(value)
    print("slider1_value_changed:{}".format(value))
    self.detected_image_view.detect(self.hParameter, self.hColorParameter, 
           self.template_window_size, self.search_window_size)

  def hColorParameter_changed(self, value):
    self.hColorParameter = int(value)
    print("slider1_value_changed:{}".format(value))
    self.detected_image_view.detect(self.hParameter, self.hColorParameter, 
           self.template_window_size, self.search_window_size)
     
  def template_window_size_changed(self, value):
    self.template_window = int(value)
    print("slider1_value_changed:{}".format(value))
    self.detected_image_view.detect(self.hParameter, self.hColorParameter, 
           self.template_window_size, self.search_window_size)
     
  def search_window_size_changed(self, value):
    self.search_window_size = int(value)
    print("slider1_value_changed:{}".format(value))
    self.detected_image_view.detect(self.hParameter, self.hColorParameter, 
           self.template_window_size, self.search_window_size)


#*************************************************
#    
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])

    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 900, 380)
    #main_view.resize(900, 380)
    main_view.show ()

    applet.exec_()

  except:
     traceback.print_exc()
     pass

