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

#  ZPlottingArea.py

# encodig: utf-8

import sys
import signal
import numpy as np
import traceback
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from numpy.random import rand


from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *


matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ZPlottingArea(FigureCanvas):

  # Constructor  
  def __init__(self, parent, width, height, figure=None):
    dpi = 80
    w = width /dpi
    h = height/dpi
    if figure is None:
      self.figure = plt.figure(figsize=(w, h), dpi=dpi)
    else:
      self.figure = figure
    self.figure.tight_layout()

    super(ZPlottingArea, self).__init__(self.figure)
    self.setParent(parent)

    self.show()

  def add(self, index):
    return self.figure.add_subplot(index)

  def add_subplot(self, x, y, i):
    plt.subplot(x, y, i)

  def get_figure(self):
    return self.figure
    
  def set_figure(self, fig):
    try:
      if self.figure is not None:
        plt.close(self.figure)
      self.figure = fig
    except:
      pass
 
  def close(self):
    if self.figure is not None:
      plt.close(self.figure)
      self.figure = None


  def clear(self):
    if self.figure is not None:
      #self.figure.cla()
      plt.cla()    
