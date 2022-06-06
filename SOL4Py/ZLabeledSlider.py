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
 
#  ZLabeledSlider.py

# encoding:utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
 

#Horizontallabeled slider(or trackbar)

class ZLabeledSlider(QWidget):
  # Constructor:
  # Creates a label and a slider with a label display current value of the slider.
  # This labeld slider has a width of size is a fixed_width given a parameter 
  # of this Constructor.
  
  def __init__(self, parent, title = "LabeledSlider", take_odd = False,
                     minimum=10, 
                     maximum=300, 
                     value=100, 
                     orientation = Qt.Horizontal, 
                     fixed_width = 180):
    QWidget.__init__(self, parent)
    self.title    = title
    self.take_odd = take_odd
    self.minimum  = minimum
    self.maximum  = maximum
    
    # To show integer in value text.
    self.take_integer = True
    
    self.vlayout = QVBoxLayout()

    # Create a hbox to contain a slider and corresponding value-label.   
    self.hlayout = QHBoxLayout()
           
    # Create a label.
    self.label = QLabel(self)

    # Create a hbox to contain a slider and value-label.
    self.hbox = QWidget(self)
    
    # vbox
    #   label
    #   hbox
    #     slider label(value)
    #      ....||..... value

    self.vlayout.addWidget(self.label)
    self.vlayout.addWidget(self.hbox)

    # Create a slider in hbox.
    self.slider = QSlider(self.hbox) 
    self.slider.setOrientation(orientation)
    
    # Create a value label in hbox.
    self.value   = QLabel(self.hbox)
    self.set_value_text(value)
    
    # Add a slider and a value-label to the hlayout.    
    self.hlayout.addWidget(self.slider)
    self.hlayout.addWidget(self.value)
   
    self.hbox.setLayout(self.hlayout)
    # Add value changed callback to display the current_value in value label.
    self.add_value_changed_callback(self.internal_value_changed)

    self.set_slider_title()

    # Set minimum and maximum and current value to slider.
    self.slider.setMinimum(self.minimum)
    self.slider.setMaximum(self.maximum)
    self.set_value(value)
    self.setLayout(self.vlayout)
    
    # Set minimum and maximum width to avoid auto resizing of PyQt
    self.setMinimumWidth(fixed_width)
    self.setMaximumWidth(fixed_width)


  def set_slider_title(self):
    string = self.title + ":[" + str(self.minimum) + "," + str(self.maximum) + "]"
    self.label.setText(string)

  def get_slider(self):
    return self.slider
 
  def set_take_integer(flag):
    self.take_integer(bool(flag))
 
  def set_minimum(self, value):  
    self.slider.setMinimum(value)
    self.set_slider_title()

  def set_range(self, min, max):  
    self.slider.setMinimum(min)
    self.slider.setMaximum(max)
    self.set_slider_title()

  def set_maximum(self, value):  
    self.slider.setMaximum(value)
    self.set_slider_title()

  def set_value(self, value):
    v = value
    if self.take_odd == True:
      if int( v % 2) == 0:
        v = (v * 2)/2 + 1
        
    if self.take_integer == True:
      v = int(v)
      
    self.slider.setValue(v)
    self.set_value_text(v)

  def get_value(self):
    self.slider.getValue(value)

  def set_label(self, value):
    self.label.setText(str(value))

  def set_value_text(self, text):
    # You have to convert text to string.
    self.value.setText(str(text))
        
  def add_value_changed_callback(self, callback):
    self.slider.valueChanged[int].connect(callback)

  # Internal callback which is called when self.slider value changed.
  # This will set current value of the slider to the value label.
  def internal_value_changed(self, value):
    v = value
    if self.take_odd == True:
      if int (v % 2) == 0:
        v = (v * 2)/2 + 1
      if self.take_integer == True:
        v = int(v)
    
    self.value.setText(str(v))
    #print("internal value changed:{}".format(v))
       

