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

#  NonPhotorealisticRendering.py

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
from SOL4Py.ZLabeledFileComboBox import ZLabeledFileComboBox


class MainView(ZApplicationView):
  # Inner classes
  #--------------------------------------------
  class SourceImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)

    def load(self, filename):
      self.load_opencv_image(filename)
      self.update()
      
  class NonPhotorealisticView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)

    def load(self, filename):
      self.load_opencv_image(filename)
      self.update()
         
    def transform(self, renderer_type_id):
      print("transform {}".format(renderer_type_id))
      try:
        src_image = self.get_opencv_image()
        self.transformed_image = None

        if src_image.any() != None:
          if renderer_type_id == MainView.EdgePreserveSmoothingByNormalizedConvolutionFilter: 
            self.transformed_image = cv2.edgePreservingFilter(src_image, flags=1)
        
          if renderer_type_id ==  MainView.EdgePreserveSmoothingByRecursiveFilter:
            self.transformed_image =  cv2.edgePreservingFilter(src_image, flags=2)

          if renderer_type_id ==  MainView.DetailEnhancement:
            self.transformed_image =  cv2.detailEnhance(src_image)
        
          if renderer_type_id ==  MainView.MonochromePencilSketch:
            self.transformed_image, _ = cv2.pencilSketch(src_image, sigma_s=10 , sigma_r=0.1, shade_factor=0.03)

          if renderer_type_id ==  MainView.ColorPencilSketch:
            _, self.transformed_image =  cv2.pencilSketch(src_image, sigma_s=10 , sigma_r=0.1, shade_factor=0.03)
          
          if renderer_type_id ==  MainView.Stylization:
            self.transformed_image =  cv2.stylization(src_image)
      
          if self.transformed_image.all() != None:
            self.set_opencv_image(self.transformed_image)
            self.update()
      except:
        traceback.print_exc()
  #--------------------------------------------
  
  
  # Class variables
  EdgePreserveSmoothingByNormalizedConvolutionFilter = 0
  EdgePreserveSmoothingByRecursiveFilter             = 1
  DetailEnhancement                                  = 2    
  MonochromePencilSketch                             = 3 
  ColorPencilSketch                                  = 4
  Stylization                                        = 5


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    self.filename = "../images/Figure.png"
    
    # 1 Create source imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create NonPhotorealisticView imageview.
    self.transformed_image_view = self.NonPhotorealisticView(self) 
    
      
    # 3 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)
    self.add(self.transformed_image_view)

    # 4 Add a labeled combobox to top dock area
    self.add_renderer_combobox()

    # 5 Load the file
    self.load_file(self.filename)
    
    self.show()
    
  def add_renderer_combobox(self):
    self.renderer_id = MainView.EdgePreserveSmoothingByNormalizedConvolutionFilter
    self.renderer_combobox = ZLabeledComboBox(self, "RenderingType", Qt.Horizontal)
    
    self.renderers = {"EdgePreserve Smoothing By Normalized Convolution Filter":
                          MainView.EdgePreserveSmoothingByNormalizedConvolutionFilter,
                     "EdgePreserve Smoothing By Recursive Filter":
                          MainView.EdgePreserveSmoothingByRecursiveFilter,
                     "Detail Enhancement":                                       
                          MainView.DetailEnhancement,       
                     "Monochrome Pencil Sketch":                                 
                          MainView.MonochromePencilSketch,
                     "Color Pencil Sketch":                                      
                          MainView.ColorPencilSketch,
                     "Stylization":                                              
                          MainView.Stylization }

    self.renderer_combobox.add_items(self.renderers.keys())
    self.renderer_combobox.add_activated_callback(self.renderer_activated)
    self.renderer_combobox.set_current_text(self.renderer_id)
    
    self.set_top_dock(self.renderer_combobox)
  
    

  # Show FileOpenDialog and select an image file.
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.filename = filename
    self.source_image_view.load(filename)
    self.transformed_image_view.load(filename)
    self.transformed_image_view.transform(self.renderer_id)

    self.set_filenamed_title(filename)
    
  def renderer_activated(self, text):
    print("renderer_activated {} {}".format(text, self.renderer_id))
    self.renderer_id = self.renderers[text]
    self.transformed_image_view.transform(self.renderer_id)
    

#*************************************************
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 800, 500)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

