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

#  FileBrowser.py
 
# encodig: utf-8

import sys
import os
import traceback

import errno

sys.path.append('../')

from SOL4Py.ZApplicationView import *


class MainView(ZApplicationView):
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height, Z.Vertical)

    self.treeview = QTreeView()
    self.model = QFileSystemModel(self.treeview)
    self.model.setReadOnly(False)
    root = self.model.setRootPath("/")
    self.treeview.setModel(self.model)
    self.treeview.setRootIndex(root)

    self.add(self.treeview)
    
    self.treeview.clicked.connect(self.clicked)
    self.treeview.doubleClicked.connect(self.doubleClicked)

    self.show()


  def doubleClicked(self, signal):
    print(signal)
    #QModelIndex index
    file_path=self.model.filePath(signal)
    print("doubleClicked: " + file_path)


  def clicked(self, index):
    print(index)
    #QModelIndex index
    file_path=self.model.filePath(index)
    print("clicked: " + file_path)
        

#*************************************************
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 640, 480)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()


class Browser(QWidget):
    def __init__(self):
        super(Browser, self).__init__()
        self.treeview = QTreeView()
        self.model = QFileSystemModel(self.treeview)
        self.model.setReadOnly(False)
        root = self.model.setRootPath("/")
        self.treeview.setModel(self.fileSystemModel)
        self.treeview.setRootIndex(root)

        Layout = QVBoxLayout(self)
        Layout.addWidget(self.treeView)
        self.setLayout(Layout)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Browser()
    main.show()
    sys.exit(app.exec_())