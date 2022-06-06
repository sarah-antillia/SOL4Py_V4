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

#  ZLabeledSpinBox.py

# encoding:utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
 

#Horizontallabeled spinbox

class ZLabeledDoubleSpinBox(QWidget):
  # Constructor:
  # Creates a  spinbox with a label 
  
  def __init__(self, parent, label = "LabeledSpinBox", 
                     minimum=0, 
                     maximum=20, 
                     value=10, 
                     step =1,
                     fixed_width = 180):
    QWidget.__init__(self, parent)
    self.minimum  = minimum
    self.maximum  = maximum

    # Create a hbox to contain a spinbox and value-label.
    self.hlayout =  QHBoxLayout()

    # Create a label and spinbox.
    self.label  = QLabel(self)
    self.label.setText(label)
    self.spinbox = QDoubleSpinBox(self) 
    self.spinbox.setSingleStep(step)
    self.spinbox.setRange(self.minimum, self.maximum)
    self.spinbox.setValue(value)
    
    self.hlayout.addWidget(self.label)
    self.hlayout.addStretch()
    self.hlayout.addWidget(self.spinbox)
    self.setLayout(self.hlayout)


  def add_value_changed_callback(self, callback):
    self.spinbox.valueChanged(callback)


  def get_spinbox(self):
    return self.spinbox


  def get_value(self):
    return self.spinbox.value()

  def set_value(self):
    return self.spinbox.setValue()


  def set_range(self, min, max):  
    self.spinbox.setRange(min, max)


  def set_label(self, value):
    self.label.setText(str(value))
        


