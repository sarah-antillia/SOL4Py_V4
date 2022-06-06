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

#  ZScrolledPlottingArea.py
 
# 2018/05/05 Updated

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno


from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from SOL4Py.Z3DPlottingArea  import *


class ZScrolled3DPlottingArea(QScrollArea):

  def __init__(self, parent, width, height):
    super(ZScrolled3DPlottingArea, self).__init__(parent)
    self.plotting_area = Z3DPlottingArea(self, width, height)
    self.setWidget(self.plotting_area)
   
  def add(self, index):
    return self.plotting_area.add(index)
    
  def get_plotting_area(self):
    return self.plotting_ara
    
  def get_figure(self):
    return self.plotting_area.get_figure()
    
  def get_ax(self):
    return self.plotting_area.get_ax()
    
