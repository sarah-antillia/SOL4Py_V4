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

#  CelledScrolledImageView.py

# encodig: utf-8

import sys
import os
import cv2
import traceback

# 
sys.path.append('../')

from SOL4Py.ZApplicationView import *
from SOL4Py.ZScrolledImageView  import ZScrolledImageView
from SOL4Py.ZVerticalPane    import ZVerticalPane 
 
class MainView(ZApplicationView):

  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    filename1 = "../images/flower.png"
    filename2 = "../images/flower3.jpg"
    
    # 1 Create the first imageview.
    self.image_views = [None, None]
    self.image_views[0] = ZScrolledImageView(self, 0, 0, width/2, height)

    # 2 Create the second imageview.
    self.image_views[1] = ZScrolledImageView(self, 0, 0, width/2, height)

    # 2 Add the image view to a main_layout of this main view.
    for i in range (len(self.image_views)):
       self.add(self.image_views[i])

    # 3 Load the file
    self.load_file(filename1, 0)
    self.load_file(filename2, 1)
      
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
    
  # Show FileOpenDialog and select an image file.
  def first_file_open(self):
    self.file_open(0)

  def second_file_open(self):
    self.file_open(1)
    
  def file_open(self, index):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename, index)
      
  def load_file(self, filename, index):
    self.image_views[index].load_image(filename)    
    self.set_filenamed_title(filename)
      

#*************************************************
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 1000, 460)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()


