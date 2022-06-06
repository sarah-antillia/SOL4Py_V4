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
 
#  MultipleScrolledFigureViewer.py

# encodig: utf-8

import sys
import os
import cv2
import traceback

import seaborn as sns
from sklearn import datasets
import matplotlib.pyplot as plt

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

# 
sys.path.append('../')

from SOL4Py.ZApplicationView import *
from SOL4Py.ZScrolledFigureView  import ZScrolledFigureView
from SOL4Py.ZVerticalPane    import ZVerticalPane 
 
class MainView(ZApplicationView):

  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
    
    # 1 Create three figure view.
    self.image_views = [None, None, None]
    num = len(self.image_views)

    for i in range(num):
      self.image_views[i] = ZScrolledFigureView(self, 0, 0, width/num, height)
      self.add(self.image_views[i])

    # 2 Set plt figures
    self.set_figures()
    
    self.show()

  def set_figures(self):
    # 1 Flight heatmap
    sns.set()
    plt.title("Flights Heatmap")
    flights = sns.load_dataset("flights")
    flights = flights.pivot("month", "year", "passengers")
    sns.heatmap(flights, annot=True, fmt="d")
    plt.tight_layout()
    self.image_views[0].set_figure(plt)
    
    # 2 Iris pairplot
    iris = sns.load_dataset("iris")
    sns.set()
    sns.pairplot(iris, hue="species", size=3.0)
    plt.title("Iris Pairplot")

    self.image_views[1].set_figure(plt)    

    # 3 Iris swarmplot
    plt.title("Iris Swarmplot")
    sns.set()
    sns.swarmplot(x="species", y="petal_length", data=iris)
    
    self.image_views[2].set_figure(plt)    


#*************************************************
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 1000, 460)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()


