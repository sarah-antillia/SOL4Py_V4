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

# 2019/05/10

# TrainingProcessLossMonitor.py
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


sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZPlottingArea  import *
from SOL4Py.keras.ZEpochLogServer import *


class MainView(ZApplicationView):

  ## Inner class starts.
  class EpochLogServer(ZEpochLogServer):

    ##
    # Constructor
    def __init__(self, view, ipaddress, port):
      ZEpochLogServer.__init__(self, ipaddress, port)
      # The values loss and acc may be plotted on figure of matplotlib
      self.view   = view
      self.clear()


    def clear(self):
      print("clear")

      self.x = []
      self.y_loss     = []
      self.y_val_loss = []
      self.max_loss  = 3
      
      self.x.append(0.0)
      self.y_loss.append(0.0)
      self.y_val_loss.append(0.0)
  
      self.update_loss_plotting()
      

    # 
    def request_handle_callback(self, bytes, writer):
      print(__class__.__name__ + "::" + __class__.request_handle_callback.__name__ + " start")
      text = bytes.decode("utf-8")
      print(text)
      if "on_train_begin" in text:
        if ":" in text:
          _, notifier, epochs = text.split(":")
          self.view.set_filenamed_title(notifier)
          self.view.update_epochs(int(epochs))
          
        self.clear()
 

      if "," in text:
        epoch, loss, val_loss = text.split(",")
        print("{}  {} {} ".format(epoch, loss, val_loss))

        self.x.append(int(epoch))
        self.y_loss.append(float(loss))
        self.y_val_loss.append(float(val_loss))
        self.update_loss_plotting()


    def update_loss_plotting(self):
      v1 = self.max_loss
      v2 = self.max_loss
       
      if len(self.y_loss) > 1:
        v1 = self.y_loss    [np.argmax(self.y_loss)]
      
      if len(self.y_val_loss) > 1:
        v2 = self.y_val_loss[np.argmax(self.y_val_loss)]
     
      print("loss v1:{} v2:{}".format(v1, v2))
         
      max_loss = v1
      if v2 > v1:
        max_loss= v2
        
      self.view.update_loss_max(max_loss)
      
      self.view.update_plotter(self.x, self.y_loss,     'red')
      self.view.update_plotter(self.x, self.y_val_loss, 'blue')
 
  ## Inner class ends.
  
  
  
  ##
  # Constructor
  def __init__(self, title, x, y, width, height, epochs=40, loss=3, ipaddress="127.0.0.1", port= 8888):
    super(MainView, self).__init__(title, x, y, width, height)

    self.epochs   = epochs # epoch
    self.stride   = 1.0
    self.accuracy = 1.0
    self.loss     = loss # Default loss_max
 
    plt.subplots_adjust(wspace=0.4, hspace=0.8)
    
    # Create a loss plotting area.
    self.plotter = ZPlottingArea(self, width, height)
    
    self.ax  = self.plotter.add(111)
    self.ax.set_title("Training and validation loss")

    self.ax.set_xlim(0, self.epochs)
    self.ax.set_ylim(0, self.loss)
    self.ax.set_xlabel("epoch")
    self.ax.set_ylabel("loss")
    
    self.add(self.plotter)

    self.show()

    # Create an EpochLogServer thread and start it.
    self.thread = self.EpochLogServer(self, ipaddress = ipaddress, port= port)
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


  # Plotting training and validation loss
  def update_plotter(self, xs, ys, color):
    self.ax.plot(xs, ys, color=color,  linestyle='solid')
    self.ax.legend(["training_loss", "validation_loss"])
    self.plotter.draw()


  def update_epochs(self, epochs):
    self.epochs = epochs
    self.ax.set_xlim(0, self.epochs)


  def update_loss_max(self, loss_max):
    self.ax.set_ylim(0, loss_max)
  
  def clear(self):
    self.plotter.clear()

  def file_quit(self):
    self.thread.close()
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
    argc   = len(sys.argv)
    epochs = 40
    loss   = 3
    
    if argc == 2:
      epochs = int(sys.argv[1])
    if argc == 3:
      epochs = int(sys.argv[1])
      loss   = int(sys.argv[2])

    applet = QApplication(sys.argv)

    mainv = MainView(name, 40, 80, 600, 400, epochs= epochs, loss= loss, ipaddress="127.0.0.1", port= 8888)
    mainv.show()

    applet.exec_()
    
  except:
    traceback.print_exc()
  else:
    pass
    
  finally:
   pass
      
