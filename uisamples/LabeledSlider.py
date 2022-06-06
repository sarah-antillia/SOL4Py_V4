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
# 
#  LabeledSlider.py


# encodig: utf-8

import sys
import os
import cv2
import traceback

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

sys.path.append('../')

from SOL4Py.ZLabeledSlider  import ZLabeledSlider
## 
# MainView class to test ZLabeledSlider.
# This inherits QMainWindow.
  
class MainView(QMainWindow):
  def __init__(self, title, parent=None):
    super(MainView,self).__init__( parent)
    self.setWindowTitle(title)

    # 1. Create main_vbox and main_vlayout
    self.main_vbox    = QWidget(self)
    self.main_vlayout = QVBoxLayout(self.main_vbox)
    self.main_vlayout.setAlignment(Qt.AlignTop)
      
    # 2, Create labeled_slider in main_vbox
    self.labeled_slider = ZLabeledSlider(self.main_vbox,take_odd=False,
                     minimum=10, 
                     maximum=300, 
                     value=100, 
                     orientation = Qt.Horizontal, 
                     fixed_width = 180)
    self.labeled_slider.add_value_changed_callback(self.slider_value_changed)
      
    self.labeled_slider.set_range(0, 200)
    self.labeled_slider.set_value(100)
      
    # 3. Add labeled_slider to main_vlayout.
    self.main_vlayout.addWidget(self.labeled_slider)
        
    self.labeled_slider.setGeometry(0, 0, 160, 70)
    self.setCentralWidget(self.main_vbox)

    self.show()

  # Callback for the slider in ZLabeledSlider.
  def slider_value_changed(self, value):
    self.labeled_slider.set_value_text(str(value))
    print("MainView.slider_value_changed:{}".format(value))

  def get_labeled_slider(self):
    return self.labeled_slider
 
###
if __name__== "__main__":
  try:
    program = sys.argv[0]
    applet = QApplication(sys.argv)
    main_view = MainView(program)
    
    main_view.resize(400, 300)
    main_view.show()
    
    applet.exec_()
    
  except:
      traceback.print_exc()
      
  sys.exit(0)
    
