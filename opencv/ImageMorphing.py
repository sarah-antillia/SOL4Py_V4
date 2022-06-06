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

#  ImageMorphing.py

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

  class TransformedImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)
      
    def load(self, filename):
      self.load_opencv_image(filename)
             
    def transform(self, shape_id, type_id,  ksize):
      src_image = self.get_opencv_image()
      
      element = cv2.getStructuringElement(shape_id,
                       (ksize, ksize), ( -1, -1) )
      transformed_image = cv2.morphologyEx(src_image, type_id, element);
      
      if transformed_image.all() != None:
        self.set_opencv_image(transformed_image)
        self.update()
      
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/HelloWorld.png"
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.transformed_image_view = self.TransformedImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
      
    # 4 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)
    self.add(self.transformed_image_view)
    
    self.show()
  

  def add_control_pane(self, fixed_width=220):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)

    self.ksize = 3

    self.shape_id = 2; 
    self.type_id  = 3
    self.shapes = { "MORPH_RECT":  0, "MORPH_CROSS": 1, "MORPH_ELLIPSE":2}
     
    self.shape = ZLabeledComboBox(self.vpane, "MorphShape")
    self.shape.add_items(list(self.shapes.keys() ))
    self.shape.add_activated_callback(self.shape_activated)
    self.shape.set_current_text(self.shape_id)
    
    self.types = { "MORPH_OPEN":   0, "MORPH_CLOSE":    1, "MORPH_GRADIENT": 2,
                   "MORPH_TOPHAT": 3, "MORPH_BLACKHAT": 4 }
    self.type = ZLabeledComboBox(self.vpane, "MorphType")
    self.type.add_items(list(self.types.keys() ))
    self.type.add_activated_callback(self.type_activated)
    self.type.set_current_text(self.type_id)
    
    self.ksize_slider = ZLabeledSlider(self.vpane, "KernelSize", take_odd =True,  
              minimum=1, maximum=33, value=self.ksize, fixed_width=200)
    self.ksize_slider.add_value_changed_callback(self.ksize_value_changed)
    
    self.vpane.add(self.shape)
    self.vpane.add(self.type)    
    self.vpane.add(self.ksize_slider)
    
    self.set_right_dock(self.vpane)

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load(filename)
    self.transformed_image_view.load(filename)    
    self.transformed_image_view.transform(self.shape_id, self.type_id, self.ksize)
    self.set_filenamed_title(filename)
      
  def shape_activated(self, text):
    self.shape_id = self.shapes[text]
    print("shape_activated:{} {}".format(text, self.shape_id))
    self.transformed_image_view.transform(self.shape_id, self.type_id, self.ksize)
     
  def type_activated(self, text):
    self.type_id = self.types[text]
    print("type_activated:{} {}".format(text, self.type_id))
    self.transformed_image_view.transform(self.shape_id, self.type_id, self.ksize)
     
  
  def ksize_value_changed(self, value):
    self.ksize = int(value)
    if self.ksize % 2 == 0:
      self.ksize = int((self.ksize * 2)/2 + 1)
      # Block size should be odd.
    #print("ksize_value_changed:{}".format(ksize))
    self.transformed_image_view.transform(self.shape_id, self.type_id, self.ksize)
     
 
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
    

