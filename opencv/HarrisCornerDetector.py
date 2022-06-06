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

#  HarrisCornerDetector.py
# 2018/08/24

# encodig: utf-8

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
      
    def load(self, filename):
      source_image = self.load_opencv_image(filename)
      self.gray_image = cv2.cvtColor(source_image, cv2.COLOR_RGB2GRAY)
    
    #The following detect_cornert method  is based on the code:
    #http:#www.swarthmore.edu/NatSci/mzucker1/opencv-2.4.10-docs/
    #  doc/tutorials/features2d/trackingmotion/harris_detector/harris_detector.html
             
    def detect(self, bsize, ksize, threshold):
      source_image = self.get_opencv_image()
      
      #blockSize: Neighborhood size.

      #ksize : Aperture parameter for the Sobel operator, 
      # which should be odd.
      ksize = int(ksize)

      #k: Harris detector free parameter.
      k = float(0.04)
      w, h, c = source_image.shape
      dest_image  = np.zeros([w, h], dtype=np.uint8 )
      gray_image = cv2.cvtColor(source_image, cv2.COLOR_RGB2GRAY)

      dest_image = cv2.cornerHarris(gray_image, bsize, ksize, k, cv2.BORDER_DEFAULT )

      cv2.normalize(dest_image, dest_image, 0, 255, cv2.NORM_MINMAX)

      #We draw circles at the corners detected by cornerHarris on the originalImage 
      # by using the destNormalized image data and the threshold parameter 
      # which is used to draw the circles..

      detected_image = source_image.copy() 
      iw, ih = dest_image.shape
      for j in range( iw) :
        for  i in range( ih) :
          if dest_image[j,i] > threshold :
            cv2.circle(detected_image, ( i, j ), 5,  (0, 0, 255), 1, 8, 0)

      self.set_opencv_image(detected_image)
      self.update()
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename = "../images/Geometry.png"
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.detectd_image_view = self.DetectedImageView(self) 
  
    # 3 Load the file
    self.load_file(filename)
      
    # 4 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)
    self.add(self.detectd_image_view)

    self.show()
  

  def add_control_pane(self, fixed_width=220):
    # Control pane widget

    self.vpane = ZVerticalPane(self, fixed_width)
    
    self.blockSize  = 7;
    self.kernelSize  = 5;
    self.detectorThreshold  = 100
        
    self.blockSizeance_slider = ZLabeledSlider(self.vpane, "BlockSize", take_odd =False,  
              minimum=2, maximum=100, value=self.blockSize, fixed_width=200)
    self.blockSizeance_slider.add_value_changed_callback(self.blockSizeance_value_changed)


    self.kernelSize_slider = ZLabeledSlider(self.vpane, "KernelSize", take_odd =True,  
              minimum=3, maximum=31, value=self.kernelSize, fixed_width=200)
    self.kernelSize_slider.add_value_changed_callback(self.kernelSize_value_changed)
    
    self.detectorThreshold_slider = ZLabeledSlider(self.vpane, "DetectorThreshold", take_odd =False,  
              minimum=100, maximum=240, value=self.detectorThreshold, fixed_width=200)
    self.detectorThreshold_slider.add_value_changed_callback(self.detectorThreshold_value_changed)
    
    self.vpane.add(self.blockSizeance_slider)
    self.vpane.add(self.kernelSize_slider)
    self.vpane.add(self.detectorThreshold_slider)
    
    self.set_right_dock(self.vpane)

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.source_image_view.load(filename)
    self.detectd_image_view.load(filename)
    
    self.detectd_image_view.detect(self.blockSize, self.kernelSize, self.detectorThreshold)

    self.set_filenamed_title(filename)
      
  
  def blockSizeance_value_changed(self, value):
    self.blockSize= int(value)
    self.detectd_image_view.detect(self.blockSize, self.kernelSize, self.detectorThreshold)
     
  def kernelSize_value_changed(self, value):
    self.kernelSize = int(value)
    self.detectd_image_view.detect(self.blockSize, self.kernelSize, self.detectorThreshold)

  def detectorThreshold_value_changed(self, value):
    self.detectorThreshold = int(value)
    self.detectd_image_view.detect(self.blockSize, self.kernelSize, self.detectorThreshold)


     
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

