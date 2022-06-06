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

#  ImageStitcher.py

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
from SOL4Py.ZHorizontalLayouter import ZHorizontalLayouter

class MainView(ZApplicationView):
  
  FIRST  = 0
  SECOND = 1
  THIRD  = 2
  

  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
    
    self.filenames = ["../images/Lake2.png", "../images/Lake1.png", "../images/Blank.png"]
    
    self.grid = ZGridLayouter(self)
    
    self.image_views = [None, None, None]

    flags = cv2.IMREAD_COLOR

    # 1 Create first imageview.
    self.image_views[self.FIRST]  = ZOpenCVImageView(self.grid, self.filenames[self.FIRST], flags) 
    self.image_views[self.SECOND] = ZOpenCVImageView(self.grid, self.filenames[self.SECOND], flags) 
    self.image_views[self.THIRD]  = ZOpenCVImageView(self.grid, self.filenames[self.THIRD], flags) 
    self.grid.add(self.image_views[self.FIRST],  0, 0)
    self.grid.add(self.image_views[self.SECOND], 0, 1)
    self.grid.add(self.image_views[self.THIRD],  1, 0, 1, 2)
    
    self.mode   =  False #cv2.cv.PANORAMA 
 
    #self.stitcher = cv2.createStitcher(self.mode)
    self.stitcher = cv2.Stitcher_create(self.mode)
    
    self.stitch()

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
  def add_control_pane(self, fixed_width=130):
    # Control pane widget
    self.ksize = 11
    self.vpane = ZVerticalPane(self, fixed_width)
    
    # 1 Stitcher mode selection combobox
    self.modes = {"PANORAM": 0, "SCANS": 1}
    self.labeled_combobox = ZLabeledComboBox(self.vpane, "Sticher Mode")
    self.labeled_combobox.add_activated_callback(self.mode_changed)
    self.labeled_combobox.add_items(self.modes.keys())
    
    # Stitch pushbutton
    self.stitch_button = QPushButton("Stitch", self.vpane)
    self.stitch_button.clicked.connect(self.stitch)

    self.vpane.add(self.labeled_combobox)
    
    self.vpane.add(self.stitch_button)
    self.set_right_dock(self.vpane)
    

  def first_file_open(self):
    options = QFileDialog.Options()
    self.filenames[self.FIRST], _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if self.filenames[self.FIRST]:
      self.image_views[self.FIRST].load_opencv_image(self.filenames[self.FIRST],  cv2.IMREAD_COLOR)
    filename = self.filenames[self.FIRST] + " " + self.filenames[self.SECOND]
    #self.stitch()
    
    self.set_filenamed_title(filename)
      
  def second_file_open(self):
    options = QFileDialog.Options()
    self.filenames[self.SECOND], _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if self.filenames[self.SECOND]:
      self.image_views[self.SECOND].load_opencv_image(self.filenames[self.SECOND],  cv2.IMREAD_COLOR)
    
    filename = self.filenames[self.FIRST] + " " + self.filenames[self.SECOND]
    #self.stitch()
    
    self.set_filenamed_title(filename)
      
  # combobox changed callback.
  def mode_changed(self, text):
    new_mode  = self.modes[text]
    print("prev mode {}".format(self.mode))
    if new_mode != self.mode:
      # Need to recreate stitcher object.
      self.mode = new_mode
      print("Recreated new stitcher {}".format(self.mode))
 
      self.stitcher = cv2.createStitcher(self.mode) #

    self.stitch()
    
    
  def stitch(self):
    image1 = self.image_views[self.FIRST].get_opencv_image()
    image2 = self.image_views[self.SECOND].get_opencv_image()
    if image1.all() == None  or image2.all() == None:
      QMessageBox.critical(self, "Stitcher ", "First and/or second image is empty!")
      return
        
    images = (image1, image2)
    
    status, stitched_image = self.stitcher.stitch(images, self.mode)
    
    if status == 0:
      print("Stitched two images")
      self.image_views[self.THIRD].set_opencv_image(stitched_image)
      self.image_views[self.THIRD].update()
    else:
      error = self.get_error_message(status)
      QMessageBox.critical(self, "Stitcher Failed", error)

      
  def get_error_message(self, key):
    key = str(key)
    
    status = { #"0": "OK",  
               "1": "Err_Need_More_Image",
               "2": "Err_Homography_Est_Fail",    
               "3": "Err_Camera_Params_Adjust_Fail"}
    return status[key]
 
  

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

