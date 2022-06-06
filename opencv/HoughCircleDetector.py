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

# HoughCircleDetector.py

#2018/08/25
#This is a simple example to apply cv::HoughLinesP API to
# a gray scale edged image gotten from cv::Canny API. 
# See: http://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html
 
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
      self.gray_image = None
      
    def load(self, filename):
      self.load_opencv_image(filename)
      source_image = self.get_opencv_image()
      self.gray_image = cv2.cvtColor(source_image, cv2.COLOR_RGB2GRAY)
 

    def detect(self, ksize, sigma, threshold1, paramThreshold):
      ksize = int(ksize)
      source_image = self.get_opencv_image()
     
      #1 Apply cv::GaussianBlur to the source_image.
      blurred_image = cv2.GaussianBlur(self.gray_image, (ksize, ksize), sigma, sigma)
      #2 Apply cv::HoughCircles to the grayImage to detect circles.
      w, h = blurred_image.shape
      circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT,1,
                      minDist=w/8, param1=threshold1, param2=paramThreshold, minRadius=0,maxRadius=0)
 
      if circles is not None:
        detected_image = source_image.copy()
        for circle in circles[0,:]:

          #3 Draw the center of the circle of radius = 3
          cv2.circle(detected_image, (circle[0], circle[1]), 3, (0,255,0), -1, 8, 0 )

          #4 Draw the outline of the circle of radius
          cv2.circle(detected_image, (circle[0], circle[1]), circle[2], (0,0,255), 3, 8, 0 )
     
        self.set_opencv_image(detected_image)
        
      self.update()
      
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/Geometry3.png"
    
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


  # Add control pane to MainView
  def add_control_pane(self, fixed_width=200):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)
    

    self.ksize = 3
    
    self.ksize_slider = ZLabeledSlider(self.vpane, "GaussianBlur KernelSize", take_odd =True,  
              minimum=0, maximum=31, value=self.ksize)
    self.ksize_slider.add_value_changed_callback(self.ksize_value_changed)
    
    self.vpane.add(self.ksize_slider)
    
    self.sigma = 2    
    self.sigma_slider = ZLabeledSlider(self.vpane, "GaussianBlur SigmaSize", take_odd =True,  
              minimum=1, maximum=21, value=self.sigma)
    self.sigma_slider.add_value_changed_callback(self.sigma_value_changed)
    
    self.vpane.add(self.sigma_slider)

    self.threshold1 = 120
    self.threshold2 =  50
    
    self.threshold1_slider = ZLabeledSlider(self.vpane, "CannyEdgeThreshold1", take_odd =True,  
              minimum=0, maximum=300, value=self.threshold1)    
    self.threshold1_slider.add_value_changed_callback(self.slider1_value_changed)
    self.vpane.add(self.threshold1_slider)

    self.threshold2_slider = ZLabeledSlider(self.vpane, "ParamThreshold", take_odd =True,  
              minimum=0, maximum=300, value=self.threshold2)    
    self.threshold2_slider.add_value_changed_callback(self.slider2_value_changed)
    self.vpane.add(self.threshold2_slider)

    self.set_right_dock(self.vpane)


  # Show FileOpenDialog and select an image file.
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load(filename)
    self.detected_image_view.load(filename)
    self.detected_image_view.detect(int(self.ksize), int(self.sigma), self.threshold1, self.threshold2 )
    self.set_filenamed_title(filename)
      
  # Slider value changed callback.
  def ksize_value_changed(self, value):
    self.ksize = int(value)
    if self.ksize % 2 == 0:
      self.ksize = (self.ksize * 2)/2 + 1
      # Kernel size should be odd.
    #print("slider_value_changed:{}".format(ksize))
    self.detected_image_view.detect(int(self.ksize), int(self.sigma), self.threshold1, self.threshold2 )
     
  # Slider value changed callback.
  def sigma_value_changed(self, value):
    self.sigma = int(value)
    #print("slider_value_changed:{}".format(ksize))
    self.detected_image_view.detect(int(self.ksize), int(self.sigma), self.threshold1, self.threshold2 )

  def slider1_value_changed(self, value):
    self.threshold1 = int(value)
    self.detected_image_view.detect(int(self.ksize), int(self.sigma), self.threshold1, self.threshold2 )

  def slider2_value_changed(self, value):
    self.threshold2 = int(value)
    self.detected_image_view.detect(int(self.ksize), int(self.sigma), self.threshold1, self.threshold2 )

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

