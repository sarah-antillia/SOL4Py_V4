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
from mpl_toolkits.mplot3d import Axes3D


matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Z3DPlottingArea(FigureCanvas):

  # Constructor  
  def __init__(self, parent, width, height):
    dpi = 80
    w = width /dpi
    h = height/dpi
    self.figure = plt.figure(figsize=(w, h), dpi=dpi)
    super(Z3DPlottingArea, self).__init__(self.figure)

    self.figure.tight_layout()
    self.ax = Axes3D(self.figure)
    
    #Set default axis labels.
    self.ax.set_xlabel("X")
    self.ax.set_ylabel("Y")
    self.ax.set_zlabel("Z")

    self.setParent(parent)

    self.show()

  def add(self, index):
    return self.figure.add_subplot(index)

  def get_figure(self):
    return self.figure
    
  def get_ax(self):
    return self.ax
