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

#  ZHorizontalLayouter.py

# encoding: utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
 
# Widget having a QHBoxLayout

class ZHorizontalLayouter(QWidget):
  def __init__(self, parent):
    super(ZHorizontalLayouter, self).__init__(parent)
    
    self.layout = QHBoxLayout(self)
    parent.setCentralWidget(self)
    
  def add(self, widget, x=0, y=0):
    self.layout.addWidget(widget)

  def add_widget(self, widget, x=0, y=0):
    self.layout.addWidget(widget)


  def get_layout(self):
    return self.layout
   
  def get_widget(self):
    return self

  def remove_widget(self, widget):
    self.layout.removeWidget(widget)
 
