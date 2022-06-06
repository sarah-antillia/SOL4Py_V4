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
# 
#  ImageSaultPepperNoiseInjector.py

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
from SOL4Py.ZSaultPepperNoiseInjector import *

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

  class NoisedImageView(ZOpenCVImageView):
    def __init__(self, parent):
      ZOpenCVImageView.__init__(self, parent)
      self.noised_image = None
 
    def load(self, filename):
      self.load_opencv_image(filename)
      self.update()
      
    def inject_noise(self, sault, pepper):
      src_image = self.get_opencv_image()

      injector =  ZSaultPepperNoiseInjector(sault/100.0)
      self.noised_image = injector.inject_to(src_image)
      
      self.set_opencv_image(self.noised_image)
      self.update()
      
    def get_noised_image(self):
      return self.noised_image
      
  #--------------------------------------------


        
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    self.filename = "../images/SlantCatImage.png"
    self.filename = os.path.abspath(self.filename)
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self) 

    # 2 Create second imageview.
    self.noised_image_view = self.NoisedImageView(self) 
  
    # 3 Load the file
    self.load_file(self.filename)
    
    # 4 Add imageviews to the main_layout which is a horizontal layouter.
    self.add(self.source_image_view)
    self.add(self.noised_image_view)

    self.show()


  def add_control_pane(self, fixed_width=220):
    # Control pane widget
    self.vpane = ZVerticalPane(self, fixed_width)

    self.sault        = 30
    self.sault_slider = ZLabeledSlider(self.vpane, "Sault", take_odd =False,  
                        minimum=0, maximum=100, value=self.sault)
    self.sault_slider.add_value_changed_callback(self.sault_changed)

    self.pepper        = 30
    self.pepper_slider = ZLabeledSlider(self.vpane, "Pepper", take_odd =False,  
                        minimum=0, maximum=100, value=self.sault)
    self.pepper_slider.add_value_changed_callback(self.pepper_changed)

    self.vpane.add(self.sault_slider)
    self.vpane.add(self.pepper_slider)
    self.set_right_dock(self.vpane)


  def file_open(self):
    options = QFileDialog.Options()
    self.filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if self.filename:
      self.load_file(self.filename)

  def file_save(self):
    options = QFileDialog.Options()
    dir, name = os.path.split(self.filename)
    filename = "Noised" + name
    save_filename, _ = QFileDialog.getSaveFileName(self,"FileSaveDialog-NoisedImage", filename,
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if save_filename:
      noised_image = self.noised_image_view.get_noised_image()
      cv2.imwrite(save_filename, noised_image)
    
          
  def load_file(self, filename):
    self.source_image_view.load(filename)
    self.noised_image_view.load(filename)
    self.noised_image_view.inject_noise(self.sault, self.pepper)
    self.set_filenamed_title(filename)


  def sault_changed(self, value):
    self.sault = int(value)
    #print("slider1_value_changed:{}".format(value))
    self.noised_image_view.inject_noise(self.sault, self.pepper)

  def pepper_changed(self, value):
    self.pepper = int(value)
    #print("slider1_value_changed:{}".format(value))
    self.noised_image_view.inject_noise(self.sault, self.pepper)

#*************************************************
#    
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])

    applet    = QApplication(sys.argv)

    main_view = MainView(app_name, 40, 40, 900, 380)
    #main_view.resize(900, 380)
    main_view.show ()

    applet.exec_()

  except:
     traceback.print_exc()
     pass

