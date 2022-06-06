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

#  ObjectDetectorByCacadeClassifier.py

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
      
    def detect(self, xml_classifier):
      image = self.get_opencv_image()
      try:
        cascade_classifier = cv2.CascadeClassifier()
        cascade_classifier.load(xml_classifier);
  
        faces = cascade_classifier.detectMultiScale(image,  1.3, 4) #scaleFactor=1.1, minNeighbors=1, minSize=(20,20))
    
        print
        if len(faces) == 0:
          QMessageBox.information(self, "ObjectDector",
                    "Not found objects by CascadeClassifier. detectMultiScale")
        else:
          for face in faces:
            x, y, w, h = face
            print("{} {} {} {}".format(x, y, w, h))
            cv2.rectangle(image, (x, y), 
                                 (x + w, y + h),
                                 (0, 200, 0), 3) ##, CV_AA);
          self.set_opencv_image(image)
          self.update()
      except:
        traceback.print_exc()
      
  #--------------------------------------------
  


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    self.filename = "../images/WafukuGirl.png"
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

  
    # 3 Load the file
    self.load_file(self.filename)
      
    # 4 Add two image views to a main_layout of this main view.
    self.add(self.source_image_view)

    # 5 Add a labeled file combobox to top dock area
    self.add_classifier_combobox()
            
    self.show()

  
  # Add control pane to MainView
  def add_control_pane(self, fixed_width=200):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)

    self.reload_button = QPushButton("Reload", self.vpane)
    self.reload_button.clicked.connect(self.reload_button_clicked)
    
    self.vpane.add(self.reload_button)

    self.detect_button = QPushButton("Detect", self.vpane, )
    self.detect_button.clicked.connect(self.detect_button_clicked)
    
    self.vpane.add(self.detect_button)
    
    self.set_right_dock(self.vpane)
    
  def add_classifier_combobox(self):
    self.classifier_combobox = ZLabeledFileComboBox(self, "Classfier")
    self.classifier_combobox.listup_files("C:/opencv/build/etc/haarcascades/*.xml")
    self.set_top_dock(self.classifier_combobox)
    

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
    self.set_filenamed_title(filename)
    
  def detect_button_clicked(self):
    xml_classifier = self.classifier_combobox.get_current_text_as_fullpath()
    print("detect_button_clicked {}".format(xml_classifier))
    
    self.source_image_view.detect(xml_classifier)
    

  def reload_button_clicked(self):
 
    self.load_file(self.filename)
    
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

