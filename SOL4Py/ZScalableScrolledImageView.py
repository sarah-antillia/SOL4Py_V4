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

#  ZScalableScrolledImageView.py

# encodig: utf-8

import sys
import os
import traceback

from SOL4Py.ZImageView import *
from PyQt5.QtWidgets   import *
from PyQt5.QtGui       import *
from PyQt5.QtCore      import *
from SOL4Py.ZImageView import *

from SOL4Py.ZPushButton import *
from SOL4Py.ZScaleComboBox import *
from SOL4Py.ZVerticalLayouter import *
from SOL4Py.ZScrolledImageView import *

#---------------------------------------------------------------------

class ZScalableScrolledImageView(QWidget):

  def __init__(self, parent, x, y, width, height):
    super(QWidget, self).__init__(parent)
    self.vlayout = QVBoxLayout(self)
    self.vlayout.setSpacing(0)
    self.vlayout.setContentsMargins(0,0,0,0);

    self.scale_combobox = ZScaleComboBox(self, "Scale")
    self.save_button    = ZPushButton("Save", self.scale_combobox)
    
    self.scale_combobox.add(self.save_button)
    
    self.save_button.add_activated_callback(self.save_button_activated)
    
    self.vlayout.addWidget(self.scale_combobox)
    
    self.image_view = ZScrolledImageView(parent, x, y, width, height)
    self.vlayout.addWidget(self.image_view)
    self.scale_combobox.add_activate_callback(self.scale_changed)
    
        
  def load_image(self, filename):
    self.image_view.load_image(filename) # 

  def set_plotted_figure(self):
    filename = "~temp.png"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, filename)
    plt.savefig(fullpath)
    plt.close()
    sef.image_view.load_image(fullpath)
    os.remove(fullpath)
    
    
  def get_image_view(self):
    return self.image_view

  def scale_changed(self, text):
    text = text.replace("%", "")
    scale = int(text)	# percentage
    self.image_view.rescale(scale)
    
  def update_scale(self):
    text = self.scale_combobox.get_combobox().currentText()
    self.scale_changed(str(text))
    
  def get_image(self, width, height):
    return self.image_view.get_image(width, height)
    
  def save_button_activated(self):
    #print("SaveButton clicked")
    abs_current_path = os.path.abspath(os.path.curdir)

    abs_current_path = os.path.abspath(os.path.curdir)
    files_types = "All Files (*);;Image Files (*.png;*jpg;*.jpeg)"
    filename, _ = QFileDialog.getSaveFileName(self, "FileSaveDialog", 
                             os.path.join(abs_current_path, "image.png"),
                             files_types)
    if filename:
      self.image_view.file_save(filename)

  def set_image(self, ndarray):
    self.image_view.set_image(ndarray)
    
