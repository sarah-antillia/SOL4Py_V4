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

# 2018/05/05 Updated add method.

#  ZGridLayouter.py

# encoding: utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
 
# Grid layouter which can be used as a central widget of QMainWindow. 

class ZGridLayouter(QWidget):
  def __init__(self, parent):
    super(ZGridLayouter, self).__init__(parent)
    print("ZGridLayout")
    self.layout = QGridLayout(self)
    self.setLayout(self.layout)
    
    # The parent should be an instance of QMainWindow. 
    parent.setCentralWidget(self)
    self.show()
    
    
  def add_widget(self, widget, x, y):
    print("ZGridLayout {}, {}".format(x, y))
    self.layout.addWidget(widget, x, y)
    
  # 
  def add(self, widget, x, y, spanx=1, spany=1):
    #print("ZGridLayout {}, {}".format(x, y))
    self.layout.addWidget(widget, x, y, spanx, spany)

  def get_layout(self):
    return self.layout
   
  def get_widget(self):
    return self

