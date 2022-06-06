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

#  ZLabeledCheckBox.py

# encoding:utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
 

#Horizontallabeled spinbox

class ZLabeledCheckBox(QWidget):
  # Constructor:
  # Creates a  spinbox with a label 
  
  def __init__(self, parent, label = "LabeledCheckBox", 
                     step =1,
                     fixed_width = 180):
    QWidget.__init__(self, parent)

    # Create a hbox to contain a spinbox and value-label.
    self.hlayout =  QHBoxLayout()

    # Create a label and spinbox.
    self.label  = QLabel(self)
    self.label.setText(label)
    self.checkbox = QCheckBox(self) 
    
    self.hlayout.addWidget(self.label)
    self.hlayout.addStretch()
    self.hlayout.addWidget(self.checkbox)
    self.setLayout(self.hlayout)


  def add_state_changed_callback(self, callback):
    self.checkbox.stateChanged(callback)


  def get_checkbox(self):
    return self.chekcbox


  def is_checked(self):
    return self.checkbox.isChecked()

  def set_state(self, st):
    self.checkbox.set_state(st)


  def set_label(self, value):
    self.label.setText(str(value))
        


