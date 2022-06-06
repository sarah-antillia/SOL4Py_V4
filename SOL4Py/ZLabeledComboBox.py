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

#  ZLabeledComboBox.py

# encoding: utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
 

class ZLabeledComboBox(QWidget):
  def __init__(self, parent, label, orientation=Qt.Vertical, alignment=Qt.AlignLeft, adjust_policy=True):
    #super(ZLabeledComboBox, self).__init__(parent)
    QWidget.__init__(self, parent)

    self.combobox = QComboBox(self)
    
    # 2018/05/01
    if adjust_policy == True:
      self.set_size_adjust_policy()
    
    self.label = QLabel(self)
    self.label.setText(label)
    
    if orientation == Qt.Vertical:
      self.layout = QVBoxLayout()
    if orientation == Qt.Horizontal:
      self.layout = QHBoxLayout()
      
    self.layout.addWidget(self.label)
    self.layout.addWidget(self.combobox)
    self.layout.setAlignment(alignment)
    
    self.setLayout(self.layout)

  def add(self, widget):
    self.layout.addWidget(widget)
    
  def get_combobox(self):
    return self.combobox

  def add_items(self, items):
    # 2018/05/01 Modified.
    items = list(items)
    if items != None and isinstance(items, list):
      for i in range(len(items)):  
        self.combobox.addItem(str(items[i]))

  def add_item(self, item):
    if item != None and isinstance(item, str):
      self.combobox.addItem(str(item))
    
  def get_current_text(self):
    return self.combobox.currentText()

  def set_current_text(self, index):
    self.combobox.setCurrentIndex(int(index))

  def set_label(self, value):
    self.label.setText(str(value))

  
  # Register a combobox activated callback to the self.combobox.
  def add_activated_callback(self, callback):
    self.combobox.activated[str].connect(callback)
     
  # Sample comobobox activate callback. 
  def activated(self, text):
    print("activated:{}".format(text))
        
  def set_size_adjust_policy(self):
    self.combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)    
    
  def setFont(self, font):
    self.label.setFont(font)
    self.combobox.setFont(font)
    
