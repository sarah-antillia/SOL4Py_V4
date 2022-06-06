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

#  ZColorPositioner.py

# encoding:utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

from SOL4Py.ZPositioner import * 

class ZColorPositioner(ZPositioner):
  
  def __init__(self, parent, title = "ColorPositioner", value_labels = ["R", "G", "B"],
                     minimax=[0, 255], 
                     values=[0, 128, 128], 
                     fixed_width = 260):
                     
    ZPositioner.__init__(self, parent, title, value_labels,
                     minimax, 
                     values, 
                     fixed_width)

    colors = ["red", "green", "blue"]
                         
    for i in range(3):
      self.sliders[i].setStyleSheet("QSlider::handle:horizontal {background-color:" + colors[i] + ";}")

  def set_rgb_colors(self, r, g, b):
    self.set_values([r, g, b])
    self.update()

