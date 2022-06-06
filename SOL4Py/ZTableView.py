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

#  ZTableView.py

# encodig: utf-8

import sys
import os
import traceback
import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#---------------------------------------------------------------------

class ZTableView(QWidget):

  def __init__(self, parent):
    super(ZTableView, self).__init__(parent)
    self.model = QStandardItemModel(self)

    self.tableView = QTableView(self)
    self.tableView.setModel(self.model)
    self.tableView.horizontalHeader().setStretchLastSection(True)
    self.tableView.verticalHeader().setStretchLastSection(True)
    self.tableView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
   
    self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
    self.tableView.resizeColumnsToContents()
        
  def load_csv(self, filename):

    with open(filename, "r") as file:
      for row in csv.reader(file):
        items = [
                 QStandardItem(field)
                 for field in row
        ]
        self.model.appendRow(items)
    self.tableView.resizeRowsToContents()
    self.tableView.resizeColumnsToContents()

  def resize(self, event):
    self.tableView.resizeRowsToContents()
    self.tableView.resizeColumnsToContents()

  def disable_edit(self):
    self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


