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

#  ZCSVTableView.py

# encodig: utf-8

import sys
import os
import traceback
import csv

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *


class ZCSVTableView(QTableView):
                
  def __init__(self, parent=None):
    super(QTableView, self).__init__()
        
    self.model = QStandardItemModel(parent)
    self.setModel(self.model)
    self.horizontalHeader().setStretchLastSection(True)
    self.model.setSortRole(Qt.UserRole)
 
    #parent.add(self)
    
    #self.load_file("../data/iris.csv")
    
    #self.show()

  
  def resizeToContents(self, columns):
    header = self.horizontalHeader()
    #header.setSectionResizeMode(0,   QHeaderView.Stretch)
    for i in range(columns):
      header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
  
  def strechLastSection(self, flag):
    self.horizontalHeader().setStretchLastSection(flag)

  def load_file(self, filename):
    # 1. Remove all rows from the self.model
    self.model.clear()

    # 2. Open CSV file and read lines and append those lines to the self.model.
    
    with open(filename) as f:
      reader = csv.reader(f)
      header = next(reader)                               
      self.model.setHorizontalHeaderLabels(header)

      for row in reader:
        items = []
        for column in row:
          items.append(QStandardItem(column))
        self.model.appendRow(items)


  def clear(self):
     # 1. Remove all rows from the self.model
     self.model.clear()

