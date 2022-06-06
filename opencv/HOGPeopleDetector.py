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

#  HOGPeopleDetector.py

"""
detectMultiScale(...) method of cv2.HOGDescriptor instance
    detectMultiScale(img[, hitThreshold[, 
                     winStride[, 
                       padding[, 
                         scale[, 
                         finalThreshold[, useMeanshiftGrouping
                         ]]]]]]) -> foundLocations, foundWeights
    .   @brief Detects objects of different sizes in the input image. The detected objects are returned as a list
    .   of rectangles.
    .   @param img Matrix of the type CV_8U or CV_8UC3 containing an image where objects are detected.    
    .   @param foundLocations Vector of rectangles where each rectangle contains the detected object.
    .   @param foundWeights Vector that will contain confidence values for each detected object.
    .   @param hitThreshold Threshold for the distance between features and SVM classifying plane.
    .   Usually it is 0 and should be specfied in the detector coefficients (as the last free coefficient).
    .   But if the free coefficient is omitted (which is allowed), you can specify it manually here.
    .   @param winStride Window stride. It must be a multiple of block stride.
    .   @param padding Padding
    .   @param scale Coefficient of the detection window increase.
    .   @param finalThreshold Final threshold
    .   @param useMeanshiftGrouping indicates grouping algorithm

"""

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
             
    def detect(self, hog_descriptor_id, stride):
      detected_image = self.get_opencv_image().copy()
      
      self.hog = None
      
      if hog_descriptor_id == MainView.DEFAULT:
        winSize     = (64,128)
        blockSize   = (16, 16)
        blockStride = ( 8,  8)
        cellSize    = ( 8,  8)
        nbins       = 9
        self.hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
      
      if hog_descriptor_id == MainView.DAIMLER:
        winSize     = (48, 96)
        blockSize   = (16, 16)
        blockStride = ( 8,  8)
        cellSize    = ( 8,  8)
        nbins       = 9
        self.hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDaimlerPeopleDetector())

      if hog_descriptor_id == MainView.USER_DEFINED:
        winSize     = (32, 64)
        blockSize   = ( 8,  8)
        blockStride = ( 4,  4)
        cellSize    = ( 4,  4)
        nbins       = 9
        self.hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)      
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

      (rectangles, weights) = self.hog.detectMultiScale(detected_image, hitThreshold=0, 
                        winStride=(stride, stride), 
                        padding=(0,0), 
                        scale=1.05, 
                        finalThreshold=2)
                        
      for (x, y, w, h) in rectangles:
        cv2.rectangle(detected_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

      self.set_opencv_image(detected_image)
      self.update()
      
  #--------------------------------------------
  
  DEFAULT      = 0
  DAIMLER      = 1
  USER_DEFINED = 2  

  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/Pedestrian.png"
    
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
  

  def add_control_pane(self, fixed_width=220):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)

    self.stride = 6

    self.hog_descriptor_id = self.DEFAULT; 
    
    self.hog_descriptors = {"Default":     self.DEFAULT,   
                            "Daimler":     self.DAIMLER,
                            "UserDefined": self.USER_DEFINED }
           
    self.hog_descriptor = ZLabeledComboBox(self.vpane, "HOG Descriptor")
    self.hog_descriptor.add_items(list(self.hog_descriptors.keys() ))
    self.hog_descriptor.add_activated_callback(self.hog_descriptor_activated)
    self.hog_descriptor.set_current_text(self.hog_descriptor_id)
        
    
    self.stride_slider = ZLabeledSlider(self.vpane, "WinStride", take_odd =False,  
              minimum=1, maximum=16, value=self.stride, fixed_width=180)
    self.stride_slider.add_value_changed_callback(self.stride_value_changed)
    
    self.vpane.add(self.hog_descriptor)
    self.vpane.add(self.stride_slider)

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
    self.detected_image_view.detect(self.hog_descriptor_id,  self.stride)
    self.set_filenamed_title(filename)
      
  
  def stride_value_changed(self, value):
    self.stride = int(value)
    self.detected_image_view.detect(self.hog_descriptor_id,  self.stride)
     
  def hog_descriptor_activated(self, text):
    self.hog_descriptor_id = self.hog_descriptors[text]
    print("hog_descriptor_activated:{} {}".format(text, self.hog_descriptor_id))
    self.detected_image_view.detect(self.hog_descriptor_id,  self.stride)
     
 
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
    

