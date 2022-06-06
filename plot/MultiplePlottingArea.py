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

# MultiplePlottingArea.py

# Based on the sample of https://pythondatascience.plavox.info/seaborn/heatmap

import sys
import signal
import numpy as np
import traceback
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from numpy.random import rand

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

sys.path.append('../')

from SOL4Py.ZApplicationView  import *

from SOL4Py.ZPlottingArea  import *

class MainView(ZApplicationView):
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
    
    self.plotter1 = ZPlottingArea(self, width/2, height)
    self.plotter2 = ZPlottingArea(self, width/2, height)
   
    self.ax1  = self.plotter1.add(111)
    self.ax2  = self.plotter2.add(111)

    sns.set()
    flights = sns.load_dataset("flights") 
    flights = flights.pivot("month", "year", "passengers")
    sns.heatmap(flights, annot=True, fmt="d", ax = self.ax1)
    self.add(self.plotter1)

    self.mean = [3, 3, 3] 
    self.covariance = [[1, 0, 0], [0, 1, 0],   [0, 0, 1]]
    self.data = np.random.multivariate_normal(self.mean, self.covariance, 300)
    self.ax2.scatter(self.data[:,0], self.data[:,1], self.data[:,2], color='r')
    self.add(self.plotter2)
    
    self.show()

  def file_save(self):
    try:
      abs_current_path = os.path.abspath(os.path.curdir)
      files_types = "PDF (*.pdf);;PGF (*.pgf);;PNG (*.png);;PS (*.ps);;EPS (*.eps);;RAW (*.raw);;RGBA (*.rgba);;SVG (*.svg);;SVGZ (*.svgz)"
      filename, _ = QFileDialog.getSaveFileName(self, "FileSaveDialog", 
                             os.path.join(abs_current_path, "figure.png"),
                             files_types)
      if filename:
        plt.savefig(filename) 
    except:
      traceback.print_exc()
          
if main(__name__):

  try:
    name   = sys.argv[0]
    applet = QApplication(sys.argv)

    mainv = MainView(name, 40, 40, 800, 400)
    mainv.show()

    applet.exec_()
    
  except:
    traceback.print_exc()
    
