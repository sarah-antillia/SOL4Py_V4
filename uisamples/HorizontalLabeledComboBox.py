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

 
# 2018/05/01

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

sys.path.append('../')

from SOL4Py.ZLabeledComboBox   import ZLabeledComboBox

# MainView class for Unit Test
  
class MainView(QMainWindow):
  def __init__(self, title, parent=None):
    super(MainView, self).__init__(parent)
    self.setWindowTitle(title)

    
    self.vbox = QWidget(self)
    self.vlayout = QVBoxLayout(self.vbox)
    self.vlayout.setAlignment(Qt.AlignTop)
    
    # Create labeled combobox in vbox.
    self.labeled_combobox = ZLabeledComboBox(self.vbox, "LabledCombobox", orientation=Qt.Horizontal)
    self.vlayout.addWidget(self.labeled_combobox)
  
    #self.vbox.setLayout(self.vlayout)
    self.labeled_combobox.setGeometry(0, 0, 160, 60)

    self.labeled_combobox.add_activated_callback(self.combobox_activated)
      
    self.labeled_combobox.set_label("Months")
    items = ["January", "Februaty", "March", "April", "May", "June", "July", 
             "August",  "September", "October", "November", "December"]
             
    self.labeled_combobox.add_items(items)
    
    self.setCentralWidget(self.vbox)
    self.show()

  def get_labeled_combobox(self):
    return self.labeled_combobox
    
  # comobobox activated callback. 
  def combobox_activated(self, text):
    print("MainView.combobox_activated:{}".format(text))
 
if __name__ == "__main__":   
  try:
    program = sys.argv[0]
    applet = QApplication(sys.argv)
    mainv = MainView(program)
    mainv.setGeometry(40, 40, 400, 200)
    mainv.show()
    
    applet.exec_()
  except:
    traceback.print_exc()
               
