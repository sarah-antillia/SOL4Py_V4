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

#  ZLabeledFileComboBox.py

# encoding: utf-8

import sys
import os
import glob
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

from SOL4Py.ZLabeledComboBox import *
 
# This is a special combobox to display file names matched with a file pattern
# somthing like a C:\data\images\*.png.

# This also have a push button to show a folder selection dialog.

class ZLabeledFileComboBox(ZLabeledComboBox):
  
  # Contructor
  
  def __init__(self, parent, label="LabeledFileComboBox", orientation=Qt.Horizontal):
    ZLabeledComboBox.__init__(self, parent, label, orientation)
    # Create an instance of QPushButton and add it to the layout of this combobox
    self.folder_button = QPushButton("...", self)
    self.add(self.folder_button)


  # Register a button clicked callback to the self.folder_button.  
  def add_clicked_callback(self, clicked_callback):
    self.folder_button.clicked.connect(clicked_callback)    

  # List up all files matched with a file_pattern.
  # If filenames_only was True, this combobox displays filenames, 
  # if not, full path names.
  def listup_files(self, file_pattern, filename_only=True):
    abspath = os.path.abspath(file_pattern)
    slashed = abspath.replace(os.path.sep, '/')
    self.dir, _ = os.path.split(slashed)

    files = sorted(glob.glob(slashed))
      
    self.set_label(self.dir)

    if files != None:
      self.get_combobox().clear()
      self.set_size_adjust_policy()
      
      for file in files:
        # split file into dir and name.
        if filename_only == True:
          _, name = os.path.split(file)
          self.add_item(name)
        else:
          self.add_item(filename)

  def get_current_text_as_fullpath(self):
    current_text = self.get_current_text()
    #dirname = os.path.dirname(self.dir)
    #print("Dirname {} filename {}".format(self.dir, current_text) )
    path = os.path.join(self.dir, current_text)
    slashed_path = path.replace(os.path.sep, '/')
    return slashed_path
