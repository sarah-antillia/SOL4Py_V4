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

#  CSVFileViewer.py

# encodig: utf-8

import sys
import os
import traceback
import csv


sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZCSVTableView  import *

class MainView(ZApplicationView):
                
  def __init__(self, name, x, y, width, height):
    super(MainView, self).__init__(name, x, y, width, height, Z.Vertical)
    self.csv_tableview = ZCSVTableView(self)
    self.add(self.csv_tableview)
    self.csv_tableview.load_file("../data/iris.csv")
    
    self.show()


  def load_file(self, filename):
    # 1. Remove all rows from the self.model
    self.csv_tableview.clear()
    self.csv_tableview.load_file(filename)


  def file_new(self):
    msg = "Are you sure you want to clear the table-view?"
    reply = QMessageBox.question(self, "Confirmation", 
                     msg, QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
      # 1. Remove all rows from the self.model
      self.csv_tableview.clear()

   
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.csv)", options=options)
    if filename:
      self.load_file(filename)

      self.set_filenamed_title(filename)


if main(__name__):

  try:
    name = os.path.basename(sys.argv[0])

    applet = QApplication(sys.argv)
    
    main_view  = MainView(name, 40, 40, 800, 400) 
    main_view.show ()

    applet.exec_()

  except:
     traceback.print_exc()
     pass
