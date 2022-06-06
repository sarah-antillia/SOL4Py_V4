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

#  ZScrolledImageView.py

# encodig: utf-8

import sys
import os
import traceback

from SOL4Py.ZImageView import *
from PyQt5.QtWidgets   import *
from PyQt5.QtGui       import *
from PyQt5.QtCore      import *
from SOL4Py.ZImageView import *

#---------------------------------------------------------------------

class ZScrolledImageView(QScrollArea):

  def __init__(self, parent, x, y, width, height, keepAspectRatio=True):
    super(ZScrolledImageView, self).__init__(parent)
    self.image_view = ZImageView(parent, x, y, width, height, keepAspectRatio)
    self.setWidget(self.image_view)
    
  def load_image(self, filename):
    self.image_view.load_image(filename) # 

  def set_plotted_figure(self):
    filename = "temp.png"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, filename)
    plt.savefig(fullpath)
    plt.close()
    sef.image_view.load_image(fullpath)
    os.remove(fullpath)
    

  def get_image_view(self):
    return self.image_view

  def get_image(self, width, height):
    return self.image_view.get_image(width, height)
    
  def rescale(self, percentage):
    self.image_view.rescale(percentage)
    
  def file_save(self, filename):
    self.image_view.file_save(filename)

  def set_image(self, ndarray):
    self.image_view.set_image(ndarray)
        
  