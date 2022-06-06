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

#  ShapeMatcher.py

# 2018/05/01 

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
from SOL4Py.ZGridLayouter    import ZGridLayouter

 
class MainView(ZApplicationView):

  # Inner classes
  #---------------------------------------------------------
  class BinarizedImageView(ZOpenCVImageView):
    def __init__(self, parent, filename=None, flags=cv2.IMREAD_COLOR):
      ZOpenCVImageView.__init__(self, parent, filename, flags)
      src_mage = self.get_opencv_image()
      self.gray_image =  cv2.cvtColor( src_mage, cv2.COLOR_BGR2GRAY) 
      print("BinarizedImage")
      self.binarized_image = None


    def get_binarized_image(self):
      return self.binarized_image;


    def binarize(self, threshold_type, threshold_value):
      try:
        THRESHOLD_VALUE_MAX =255
        _, self.binarized_image = cv2.threshold(self.gray_image, threshold_value, 
                     THRESHOLD_VALUE_MAX, threshold_type )
        #self.update()
        #print("bin {}".format(self.binarized_image.shape))
      
        return self.binarized_image
      except:
        traceback.print_exc()
        
  class MatchedImageView (ZOpenCVImageView):
    def __init__(self, parent, filename=None, flags=cv2.IMREAD_COLOR):
      ZOpenCVImageView.__init__(self, parent, filename, flags)

    def set_matched_image(self, image):
      self.set_opencv_image(image)
      self.update()

    def set_image(self, image):
      self.set_opencv_image(image)
      self.update()
  
  #---------------------------------------------------------
  
  FIRST  = 0
  SECOND = 1
  THIRD  = 2

  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    self.filenames = ["../images/CatImage.png", "../images/CatFace.png", "../images/Blank.png"]
    
    self.image_views = [None, None, None]

    self.grid = ZGridLayouter(self)
        
    flags = cv2.IMREAD_COLOR

    # 1 Create three image views.
    self.image_views[self.FIRST ] = self.BinarizedImageView(self, self.filenames[self.FIRST ], flags) 
    self.image_views[self.SECOND] = self.BinarizedImageView(self, self.filenames[self.SECOND], flags) 
    self.image_views[self.THIRD ] = self.MatchedImageView  (self, self.filenames[self.THIRD ], flags) 

    # 2 Add the image views to the grid layouter.
    self.grid.add(self.image_views[self.FIRST ], 0, 0)
    self.grid.add(self.image_views[self.SECOND], 0, 1)
    self.grid.add(self.image_views[self.THIRD ], 1, 0, 1, 2)

    filename = self.filenames[self.FIRST] + " " + self.filenames[self.SECOND]
    
    self.set_filenamed_title(filename)

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
    
    
  def add_control_pane(self, fixed_width=200):
    # Control pane widget
    self.threshold_value = 11
    self.vpane = ZVerticalPane(self, fixed_width)

    self.threshold_type_id  = 0
    
    self.types   = {"THRESH_BINARY":      cv2.THRESH_BINARY, 
                    "THRESH_BINARY_INV":  cv2.THRESH_BINARY_INV,
                    "THRESH_TRUNC":       cv2.THRESH_TRUNC,
                    "THRESH_TOZERO":      cv2.THRESH_TOZERO,
                    "THRESH_TOZERO_INV":  cv2.THRESH_TOZERO_INV,
                    "THRESH_OTSU":        cv2.THRESH_OTSU, 
                    "THRESH_TRIANGLE":    cv2.THRESH_TRIANGLE   }

    self.threshold_type  = ZLabeledComboBox(self.vpane, "ThresholdType")
    self.threshold_type.add_items(list(self.types.keys()) )
    self.threshold_type.add_activated_callback(self.threshold_type_activated)
    self.threshold_type.set_current_text(self.threshold_type_id)

    self.threshold_value = 60
   
    self.threshold_value_slider = ZLabeledSlider(self.vpane, "ThresholdValue", take_odd =True,  
              minimum=0, maximum=255, value=self.threshold_value, fixed_width=200)
    self.threshold_value_slider.add_value_changed_callback(self.threshold_value_changed)
    self.vpane.add(self.threshold_type)    
    self.vpane.add(self.threshold_value_slider)

    self.match_min_size =  60
    self.match_max_size = 240
    
    self.match_min_size_slider = ZLabeledSlider(self.vpane, "MatchMinSize", take_odd =True,  
              minimum=10, maximum=100, value=self.match_min_size)    
    self.match_min_size_slider.add_value_changed_callback(self.match_min_size_value_changed)

    self.match_max_size_slider = ZLabeledSlider(self.vpane, "MatchMaxSize", take_odd =True,  
              minimum=100, maximum=400, value=self.match_max_size)    
    self.match_max_size_slider.add_value_changed_callback(self.match_max_size_value_changed)

    self.vpane.add(self.match_min_size_slider)
    self.vpane.add(self.match_max_size_slider)
    
    self.clear_button = QPushButton("Clear", self.vpane)
    self.clear_button.clicked.connect(self.clear_button_clicked)

    self.match_button = QPushButton("Match", self.vpane)
    self.match_button.clicked.connect(self.match_button_clicked)
    
    self.vpane.add(self.clear_button)
    self.vpane.add(self.match_button)
      
    self.set_right_dock(self.vpane)

  def first_file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.filenames[self.FIRST] = filename
      self.image_views[self.FIRST ].load_opencv_image(filename)
      self.image_views[self.THIRD ].load_opencv_image(self.filenames[self.THIRD])
    filename = self.filenames[self.FIRST] + " " + self.filenames[self.SECOND]    
    self.set_filenamed_title(filename)

  def second_file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.filenames[self.SECOND] = filename
      self.image_views[self.SECOND].load_opencv_image(filename)
      self.image_views[self.THIRD ].load_opencv_image(self.filenames[self.THIRD])

    filename = self.filenames[self.FIRST] + " " + self.filenames[self.SECOND]
    self.set_filenamed_title(filename)
      
      
  def threshold_type_activated(self, text):
    self.threshold_type_id = self.types[text]
    self.shapeMatching()
  
  def threshold_value_changed(self, value):
    self.threshold_value = int(value)
    if self.threshold_value % 2 == 0:
      # Block size should be odd.
      self.threshold_value = int((self.threshold_value * 2)/2 + 1)
    self.shapeMatching()
  
  def match_min_size_value_changed(self, value):
    self.match_min_size = int(value)
    self.shapeMatching()

  def match_max_size_value_changed(self, value):
    self.match_max_size = int(value)
    self.shapeMatching()
    
  def clear_button_clicked(self):
    src_image    = self.image_views[self.FIRST ].get_opencv_image().copy()
    self.image_views[self.THIRD].set_image(src_image)
    
  def match_button_clicked(self):
    self.shapeMatching()
    
  # Shape matching operation to two images in image_views[self.FIRST] and image_views[self.SECOND].
  # A matched rectangle will be draw on image_views[self.THIRD].
  def shapeMatching(self):
    src_image    = self.image_views[self.FIRST ].get_opencv_image().copy()
    self.image_views[self.THIRD].set_image(src_image)

    src_bin = self.image_views[self.FIRST ].binarize(self.threshold_type_id, self.threshold_value)
    tmp_bin = self.image_views[self.SECOND].binarize(self.threshold_type_id, self.threshold_value)
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(src_bin) 
    print("labels:{}".format(nlabels))
       
    dest_image = src_image.copy();
 
    MATCHING_THRESHOLD = 0.005

    minimum = [0, 0, 0, 0] #cv2.Rect(0, 0, 0, 0)
    MIN_SIMILARITY = 1.0
    found = False;
    CV_CONTOURS_MATCH_I1  =1
    for i in range(nlabels):
      x, y, w, h, a = stats[i] 
      rect = [x, y, w, h]

      # Region of interest
      roi = src_bin[y:(y+h), x:(x+w)]

      similarity = cv2.matchShapes(tmp_bin, roi, CV_CONTOURS_MATCH_I1, 0) #method=CV_CONTOURS_MATCH_I1, parameter=0);
      if ( (w >= self.match_min_size or h >= self.match_min_size ) and 
           (w <= self.match_max_size or h <= self.match_max_size )):
        if (similarity <= MIN_SIMILARITY) :
          MIN_SIMILARITY = similarity
          minimum = rect;
          print("matching similarity={}  x={} y={} w={} h={}".format( similarity, x, y, w, h))
          found = True;
       
    if found:
      x, y, w, h = minimum
      cv2.rectangle(dest_image, (x, y), (x+w, y+h), (0, 0, 255), 3);
      self.image_views[self.THIRD].set_matched_image(dest_image)
      
  
#*************************************************
#    
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 900, 500)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

