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

# 2018/09/18

# LinePlottingByTimerThread.py
# 

import sys
import signal
import numpy as np
import traceback
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import threading
import time

from numpy.random import rand

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

sys.path.append('../')

from SOL4Py.ZApplicationView  import *

from SOL4Py.ZPlottingArea  import *

class MainView(ZApplicationView):

  ## Inner class starts.
  class ModelingThread(threading.Thread):
    # Constructor
    def __init__(self, interval, view, stride, xmax):
      threading.Thread.__init__(self)
      self.view = view
      self.tsleep = interval
      self.xs = []
      self.ys = []
      self.ys2 = []
      self.x = 0.0
      self.stride = stride
      self.xmax = xmax
      self.xs.append(self.x)
      self.ys.append(0.0)
      self.ys2.append(1.0)
      
      self.looping = True
       

    def run(self):
      print("Thread started")
      
      while self.x < self.xmax:
        if self.looping == False:
           break
        time.sleep(self.tsleep)
        self.x = self.x + self.stride
        self.xs.append(self.x)
        self.ys.append( np.random.rand(1))
        self.ys2.append(np.random.rand(1)*2.0 )
        # Update self.view since the model data self.x and self.y have been updated.
        self.view.update_plotter(self.xs, self.ys, 'red')
        self.view.update_plotter(self.xs, self.ys2, 'blue')
        #self.view.update_plotter(self.x, np.random.rand(1))
          
      print("Thread terminated")
      
    def stop(self):
      self.looping = False
  ## Inner class ends.
  
  
  ##
  # Constructor
  
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    self.sleep = 0.1
    self.xmax  = 300
    self.stride = 1.0
    
    self.plotter = ZPlottingArea(self, width, height)
  
    self.ax= self.plotter.add(111)
    self.ax.set_xlim(0, self.xmax)
    self.ax.set_ylim(0, 3.0)
   
    self.add(self.plotter)
    self.show()

    # Create a thread and start it.
    self.thread = self.ModelingThread(self.sleep, self, self.stride, self.xmax)
    self.thread.start()


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

  
  def update_plotter(self, xs, ys, color):
    self.ax.plot(xs, ys, color=color,  linestyle='solid')
    self.plotter.draw()


  def file_quit(self):
    #print("file_quitt")
    self.thread.stop()
    self.thread.join()
    print("Thread stopped")
    self.terminated = True
    self.close()

  def closeEvent(self, ce):
    # Call file_quit to terminate self.thread
    self.file_quit()

 
##############################################################
#
#          
if main(__name__):

  try:
    name   = sys.argv[0]
    applet = QApplication(sys.argv)

    mainv = MainView(name, 40, 40, 1000, 400)
    mainv.show()

    applet.exec_()
    
  except:
    traceback.print_exc()
  else:
    pass
    
  finally:
   pass
      
