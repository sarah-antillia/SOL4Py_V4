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

#  ZScaleComboBox.py

# encoding: utf-8

import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

from SOL4Py.ZLabeledComboBox import *
 

class ZScaleComboBox(ZLabeledComboBox):
  def __init__(self, parent, label):
    super(ZScaleComboBox, self).__init__(parent, label, orientation=Qt.Horizontal)
    self.current_id = 4
    self.sacle  = 50
    self.scales = ["10%", "20%", "30%", "40%","50%", "60%", "70%", "80%", "90%", "100%", "120%", "140%", "160%", "180%", "200%", "220%", 
                   "240%", "260%", "280%", "300%", "350%", "400%", "450%", "500%", "550%", "600%", "650%", "700%"]
    
    self.add_items(self.scales)
    self.set_current_text(self.current_id)

  def add_activate_callback(self, callback):
    self.add_activated_callback(callback)

  def sample_combobobox_callback(self, text):
    text = text.replace("%", "")
    self.scale = int(text)

  def set_current_scale(self, scale):
    # scale is a string with percentage character'%'
    for i in range (len(self.scales)):
      if self.scales[i] == scale:
        self.set_current_text(i)

  def current_scale(self, scale):
    scale = int(scale)
    # scale should be integer
    for i in range (len(self.scales)):
      vs = int (self.scales[i].replace("%", "") )
      if vs == scale:
        self.set_current_text(i)

    
    