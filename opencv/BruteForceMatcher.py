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

#  BruteForceMatcher.py

# See for detail: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html

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
from SOL4Py.ZHorizontalLayouter import ZHorizontalLayouter

class MainView(ZApplicationView):
  
  FIRST  = 0
  SECOND = 1
  THIRD  = 2

  DETECTOR_AKAZE = 0   
  DETECTOR_BRISK = 1
  DETECTOR_ORB   = 2
  
  SOURCE_IMAGES   = 2
  
  # MainView Construsctor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
    
    self.filenames = ["../images/Tower1.png", "../images/Tower2.png", "../images/Blank.png"]
    
    self.grid = ZGridLayouter(self)
    
    self.image_views = [None, None, None]

    flags = cv2.IMREAD_COLOR

    # Create three imageviews.
    self.image_views[self.FIRST]  = ZOpenCVImageView(self.grid, self.filenames[self.FIRST], flags) 
    self.image_views[self.SECOND] = ZOpenCVImageView(self.grid, self.filenames[self.SECOND], flags) 
    self.image_views[self.THIRD]  = ZOpenCVImageView(self.grid, self.filenames[self.THIRD], flags) 
    self.grid.add(self.image_views[self.FIRST],  0, 0)
    self.grid.add(self.image_views[self.SECOND], 0, 1)
    self.grid.add(self.image_views[self.THIRD],  1, 0, 1, 2)
    
    self.detector_id   =  self.DETECTOR_AKAZE 
 
    self.detector= None

    self.show()

  
  # Redefined add_file_menu.    
  def add_file_menu(self):
    # Typical file menu    
    self.file_menu = QMenu('&File', self)
    self.file_menu.addAction('&New',  self.file_new)
    self.file_menu.addAction('&Open First File', self.first_file_open)
    self.file_menu.addAction('&Open Second File', self.second_file_open)

    self.file_menu.addAction('&Save', self.file_save)
    self.file_menu.addAction('&Save As', self.file_save_as)
    self.file_menu.addAction('&Quit', self.file_quit)
    self.menuBar().addMenu(self.file_menu)

  # Add control pane to MainView
  def add_control_pane(self, fixed_width=200):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)
    
    # 1 Stitcher detector selection combobox
    self.detectors = {"AKAZEFeatureDetector" : self.DETECTOR_AKAZE,   
                      "BRISKFeatureDetector" : self.DETECTOR_BRISK,
                      "ORBFeatureDetector"   : self.DETECTOR_ORB}

    self.detector_id = self.DETECTOR_AKAZE
    
    self.detector_combobox = ZLabeledComboBox(self.vpane, "FeatureDetector")
    self.detector_combobox.add_activated_callback(self.detector_changed)
    self.detector_combobox.add_items(self.detectors.keys())
    self.detector_combobox.set_current_text(self.detector_id)
    
    self.best_top = {"10" : 10,   "20" : 20, "30" : 30, "40" : 40,
                     "50" : 50,   "60" : 60, "70" : 70, "80" : 80,
                     "90" : 90,   "100": 100}
    self.best_top_value = 10

    self.best_top_combobox = ZLabeledComboBox(self.vpane, "BestTopNumber")
    self.best_top_combobox.add_activated_callback(self.best_top_changed)
    self.best_top_combobox.add_items(self.best_top.keys())
    self.best_top_combobox.set_current_text(0)
    
    # Match pushbutton
    self.match_button = QPushButton("Match", self.vpane)
    self.match_button.clicked.connect(self.match_button_clicked)

    self.spacer = QLabel("", self.vpane)
    self.matched_number = QLabel("", self.vpane)
    
    self.vpane.add(self.detector_combobox)
    self.vpane.add(self.best_top_combobox)
    self.vpane.add(self.match_button)
    self.vpane.add(self.spacer)
    self.vpane.add(self.matched_number)
    
    self.set_right_dock(self.vpane)
    

  def first_file_open(self):
    options = QFileDialog.Options()
    self.filenames[self.FIRST], _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if self.filenames[self.FIRST]:
      self.image_views[self.FIRST].load_opencv_image(self.filenames[self.FIRST],  cv2.IMREAD_COLOR)
    filename = self.filenames[self.FIRST] + " " + self.filenames[self.SECOND]
    
    self.set_filenamed_title(filename)
      
  def second_file_open(self):
    options = QFileDialog.Options()
    self.filenames[self.SECOND], _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if self.filenames[self.SECOND]:
      self.image_views[self.SECOND].load_opencv_image(self.filenames[self.SECOND],  cv2.IMREAD_COLOR)
    
    filename = self.filenames[self.FIRST] + " " + self.filenames[self.SECOND]
    
    self.set_filenamed_title(filename)
      
  # Detector Combobox changed callback.
  def detector_changed(self, text):
    self.detector_id  = self.detectors[text]

    self.feature_matching()
    
  # Best_top Combobox changed callback.
  def best_top_changed(self, text):
    self.best_top_value  = int(text)
    print("Best top value {}".format(self.best_top_value))
    self.matched_number
    self.feature_matching()
    
  # Match button clicked callback  
  def match_button_clicked(self):
    self.feature_matching()

  # Feature matching operation.    
  def feature_matching(self):
    try:
      self.detector = None
      
      # 1 Create a feature detector by self.detector_id.
      if self.detector_id == self.DETECTOR_AKAZE:
        self.detector =  cv2.AKAZE_create()
        
      if self.detector_id == self. DETECTOR_BRISK:
        self.detector =  cv2.BRISK_create()
        
      if self.detector_id == self.DETECTOR_ORB:
        self.detector =  cv2.ORB_create()
        
      self.keypoints   = [None, None]
      self.descriptors = [None, None]
      self.images      = [None, None]
      
      # 2 Call dector.detectAndCompute
      for i in range(self.SOURCE_IMAGES):
        self.images[i] = self.image_views[i ].get_opencv_image()
        self.keypoints[i], self.descriptors[i] = self.detector.detectAndCompute(self.images[i], None)

      # 3 Create Brute-Force Matcher object.
      bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


      # 4 Match two descriptors by using bf_matcher.
      matches = bf_matcher.match(self.descriptors[self.FIRST], self.descriptors[self.SECOND])
      
      # 5 Update matche_number label.      
      self.total_matched_number = len(matches)
      label = "Matched Number:" + str(self.best_top_value) + "/" + str(self.total_matched_number)
      self.matched_number.setText(label)
      print("matched number {}".format(len(matches)))
    
      # 6 Sort matches by distance.  
      matches = sorted(matches, key=lambda x:x.distance)


      # 7 Call cv2.drawMatches.
      out_image = self.images[self.FIRST]
      
      matched_image = cv2.drawMatches(self.images[self.FIRST],  self.keypoints[self.FIRST], 
                                      self.images[self.SECOND], self.keypoints[self.SECOND], 
                                      matches[:self.best_top_value], out_image, flags=2)

      # 8 Set matched_image to the THIRD image_view
      self.image_views[self.THIRD].set_opencv_image(matched_image);
      self.image_views[self.THIRD].update()
      
    except:
      traceback.print_exc()


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

