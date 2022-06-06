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

#  ZPositioner.py

# encoding:utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *


#Horizontallabeled slider(or trackbar)

class ZPositioner(QWidget):
  
  ORIENTATION = Qt.Horizontal
  
  # Constructor:
  # Creates a label and a slider with a label display current value of the slider.
  # This labeld slider has a width of size is a fixed_width given a parameter 
  # of this Constructor.
  
  def __init__(self, parent, title = "Positioner", value_labels = ["X", "Y", "Z"],
                     minimax = [0, 255],
                     values=[10, 100, 128],
                     fixed_width = 260):
    QWidget.__init__(self, parent)
    #super(ZPositioner, self).__init__(parent)
    self.grid_layout = QGridLayout(self)
    self.setLayout(self.grid_layout)
    
    self.setGeometry(0, 0, fixed_width+20, 120)
    self.title   = title

    self.minimum = minimax[0]
    self.maximum = minimax[1]
    self.values  = values
        
    self.sliders = [None, None, None]
    self.labels  = [None, None, None]
    self.value_labels = value_labels
    
    for i in range(3):
      self.sliders[i] = QSlider(self)
      self.sliders[i].setOrientation(self.ORIENTATION)
      self.sliders[i].setMinimum(self.minimum)
      self.sliders[i].setMaximum(self.maximum)
      self.sliders[i].setValue(self.values[i])

      self.labels [i] = QLabel(value_labels[i] + "=" + str(self.values[i]) )

    # Create a label with a range of the sliders.
    slider_range =self.get_range()

    self.label = QLabel(self.title+ slider_range)
    self.empty = QLabel("")

    # Add self.sliders and self.labels to the self.grid-layout
    self.add_widget(self.label,              0, 0)
    self.add_widget(self.empty,              0, 1)
    for i in range(3):
      self.add_widget(self.sliders[i], i+1, 0)
      self.add_widget(self.labels[i],  i+1, 1)
    
    # Set minimum and maximum width to avoid auto-resizing of PyQt
    self.setMinimumWidth(fixed_width)
    self.setMaximumWidth(fixed_width)

    internal_callbacks = [
      self._slider_value_changed_0,
      self._slider_value_changed_1,
      self._slider_value_changed_2
      ]
    # Add self._slider-value-changed callbacks to display the current_slider values on the self.value_labels.
    for i in range(3):
      self._add_value_changed_callback(i, internal_callbacks[i])


  def set_title(self, title):
    self.title = title
    range = self.get_range()
    self.label = QLabel(self.title+ range)


  def set_range(self, min, max):
    self.minimum = min
    self.maximum = max
    range = self.get_range()
    self.label = QLabel(self.title+ range)
    self.label.update()
    

  def get_range(self):
    slider_range = " :[" + str(self.minimum) + " ," + str(self.maximum) + "]"
    return slider_range


  def set_value_labels(self, labels):
    if len(labels) == 3:
       self.value_labels = labels


  def set_values(self, values):
    if len(values) == 3:
      for i in range(3):
        self.sliders[i].setValue(values[i])

  def set_position(self, values):
    self.set_values(values)
    self.update()


  def add_widget(self, widget, x, y):
    self.grid_layout.addWidget(widget, x, y)

  # This can be used to register a common slider_value_changed callback for the self.sliders
  def add_value_changed_callback(self, slider_value_changed_callback):
    for i in range(3):
      self.sliders[i].valueChanged[int].connect(slider_value_changed_callback)


  def get_values(self):
    values = [0, 0, 0]
    for i in range(3):
      values[i] = self.sliders[i].value()
    
    return values


  ## Internal private methods
  def _slider_value_changed_0(self, value):
    self.labels[0].setText(self.value_labels[0] +  "=" + str(value))


  def _slider_value_changed_1(self, value):
    self.labels[1].setText(self.value_labels[1] +  "=" + str(value))


  def _slider_value_changed_2(self, value):
    self.labels[2].setText(self.value_labels[2] +  "=" + str(value))


  def _add_value_changed_callback(self, i, callback):
    self.sliders[i].valueChanged[int].connect(callback)

