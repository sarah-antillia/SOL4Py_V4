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

#  GrayScaleImageView.py

# encodig: utf-8

import sys
import os
import traceback

sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.opencv.ZOpenCVImageView  import *
 
class MainView(ZApplicationView):
  
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
      
    filename = "../images/flower.png"

    self.image_views = [None, None]

    self.flags = [cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCALE]

    for i in range(len(self.image_views)):
      self.image_views[i]  = ZOpenCVImageView(self)
      self.add(self.image_views[i])
    
    self.load_image(filename)
    
    self.show()
           
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_image(filename)
  
  def load_image(self, filename): 
    for i in range(len(self.image_views)):
      self.image_views[i]. load_opencv_image(filename, self.flags[i])
    
    self.set_filenamed_title(filename)

####
if main(__name__):
  try:
    name  = os.path.basename(sys.argv[0])
    applet= QApplication(sys.argv)
    
    mainv = MainView(name, 40, 40, 800,360)
    mainv.show ()
    
    applet.exec_()

  except:
    traceback.print_exc()

