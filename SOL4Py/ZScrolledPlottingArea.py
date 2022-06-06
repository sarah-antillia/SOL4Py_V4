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
# 2018/08/30 Added gcf parameter to Constructor:
#  def __init__(self, parent, width, height, gcf=False):

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno


from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from SOL4Py.ZPlottingArea  import *


class ZScrolledPlottingArea(QScrollArea):
  # 2018/08/30 Added gcf parameter
  def __init__(self, parent, width, height, figure=None):
    super(ZScrolledPlottingArea, self).__init__(parent)
 
    self.plotting_area = ZPlottingArea(self, width, height, figure)
    self.setWidget(self.plotting_area)
    
  def add(self, index):
    return self.plotting_area.add(index)
    
  def get_plotting_area(self):
    return self.plotting_ara
    
  def get_figure(self):
    return self.plotting_area.get_figure()
    
  def set_figure(self, figure):
    self.setWidget(None)
    self.plotting_area.deleteLater()
    self.update()
    size = self.plotting_area.size()
    
    self.plotting_area =  ZPlottingArea(self, size.width(), size.height(), figure)
    self.setWidget(self.plotting_area)
    
    
  def clear(self):
    self.plotting_area.clear()
    self.update()

  def subplot(self, x, y, i):
    self.plotting_area.subplot(x, y, i)
    
