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

#  ApplicationViewiew.py

# encodig: utf-8

import sys
import os
import traceback


sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZLabeledFileComboBox import ZLabeledFileComboBox


class MainView(QMainWindow):
  # Constructor
  def __init__(self, name):
     QMainWindow.__init__(self)
     self.setWindowTitle(name)
     self.hbox = QWidget(self)
     self.hlayout = QHBoxLayout(self.hbox)
     self.hlayout.setAlignment(Qt.AlignRight)
     self.label   = QLabel("          ", self.hbox)
     self.label.setMinimumWidth(300)
     self.label.setMaximumWidth(300)
     
     self.pushb = QPushButton("...", self.hbox)
     
     self.pushb.clicked.connect(self.button_clicked)
     
     self.hlayout.addWidget(self.label)
     self.hlayout.addWidget(self.pushb)     
     self.setCentralWidget(self.hbox)

  def button_clicked(self):
    dir = QFileDialog.getExistingDirectory(self,
                                               'OpenFolder',
                                               os.path.expanduser('.'),
                                               QFileDialog.ShowDirsOnly)
    if dir:
      #dir = dir.replace('/', os.sep)
      print("Folder button clicked {}".format(dir))
      self.label.setText(dir)
         
if main(__name__):

  try:
    name = os.path.basename(sys.argv[0])

    applet = QApplication(sys.argv)
        
    main_view  = MainView(name)
    main_view.setGeometry(40, 40, 600, 100)
 
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()


