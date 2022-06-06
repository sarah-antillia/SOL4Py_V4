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

#  HoughLineDetector.py

#2018/08/25
#This is a simple example to apply cv::HoughLinesP API to
# a gray scale edged image gotten from cv::Canny API. 
# See: http://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html
#
# See also: Opencv python HoughLinesP strange results
# https://stackoverflow.com/questions/36452491/opencv-python-houghlinesp-strange-results

import sys
import os
import cv2
import traceback
import numpy as np

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
      self.gray_image = None
      
    def load(self, filename):
      self.load_opencv_image(filename)
      source_image = self.get_opencv_image()
      self.gray_image = cv2.cvtColor(source_image, cv2.COLOR_RGB2GRAY)
   
    def detect(self, threshold1, threshold2):
      source_image = self.get_opencv_image()
    
      #1 Apply cv::Canny to the grayImage to get edges in the grayImage.

      detected_image  = cv2.Canny(self.gray_image, threshold1=float(threshold1), threshold2=float(threshold2), apertureSize = 3)
              
      #2 Apply HoughLinesP to detectedImage returned by cv::Canny.  
      minLineLength = 100
      maxLineGap = 10
      lines = cv2.HoughLinesP(detected_image, rho=1, theta=np.pi/180, threshold=80, minLineLength=30, maxLineGap=10)
        
      #3 Put a clone of the source_image to the detected_image, 
      detected_image = source_image.copy()
        
      #4 Draw lines on the clone of the original image.
      if lines is not None:
        for line in lines:
          #In case of OpenCV3.4 
          x1, y1, x2, y2 = line[0]
          print( x1,y1,x2,y2)
          cv2.line( detected_image, (x1, y1), (x2, y2), (0, 255, 0), 2);
          
        self.set_opencv_image(detected_image)
       
      self.update()
      
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/GinzaWako.png"
        
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.detected_image_view = self.DetectedImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
    
    # 4 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)
    self.add(self.detected_image_view)

    self.show()
  

  def add_control_pane(self, fixed_width=200):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)
 
    self.threshold1 = 120
    self.threshold2 = 130
    
    self.threshold1_slider = ZLabeledSlider(self.vpane, "Threshold1", take_odd =True,  
              minimum=0, maximum=300, value=self.threshold1)    
    self.threshold1_slider.add_value_changed_callback(self.slider1_value_changed)
    self.vpane.add(self.threshold1_slider)

    self.threshold2_slider = ZLabeledSlider(self.vpane, "Threshold2", take_odd =True,  
              minimum=0, maximum=300, value=self.threshold2)    
    self.threshold2_slider.add_value_changed_callback(self.slider2_value_changed)
    self.vpane.add(self.threshold2_slider)
    
    self.set_right_dock(self.vpane)

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load  (filename)
    self.detected_image_view.load(filename)
    
    # Apply detect method to the detected image view.
    self.detected_image_view.detect(self.threshold1, self.threshold2)
    
    self.set_filenamed_title(filename)
      
  
  def slider1_value_changed(self, value):
    self.threshold1 = int(value)
    self.detected_image_view.detect(int(self.threshold1), int(self.threshold2))

  def slider2_value_changed(self, value):
    self.threshold2 = int(value)
    self.detected_image_view.detect(int(self.threshold1), int(self.threshold2))
     
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

